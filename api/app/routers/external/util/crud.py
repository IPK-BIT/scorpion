from neontology import GraphConnection
from pydantic import ValidationError
from utils.influx import write_api, Point, bucket, org, query_api
import math
from utils import models, schemas, responses

from icecream import ic

def get_all_providers(skip: int, limit: int):
    db_providers=models.ServiceProvider.match_nodes(skip=skip, limit=limit)
    total_providers=len(models.ServiceProvider.match_nodes())
    results = []
    for db_provider in db_providers:
        results.append(schemas.ServiceProvider(
            abbreviation=db_provider.providerAbbr, 
            name=db_provider.providerName
        ))
    return responses.Response(
        metadata=schemas.Metadata(
            currentPage=skip/limit,
            pageSize=limit,
            totalCount=total_providers,
            totalPages=math.ceil(total_providers/limit)
        ),
        result=results
    )

def get_providers_by_user(user_id: str, skip: int, limit: int):
    cypher=f"""
    MATCH (u:USER)-[:IS_MEMBER {{approved: 1}}]->(p:ServiceProvider)
    WHERE u.id=$user_id
    RETURN p
    """
    params = {
        "user_id": user_id
    }
    graph = GraphConnection()
    records = graph.cypher_read_many(cypher, params)
    results:list[schemas.ServiceProvider] = []
    ctr = 0
    for idx, record in enumerate(records):
        if (idx>=skip and idx<limit+skip):
            results.append(schemas.ServiceProvider(
                abbreviation=record["p"]["providerAbbr"],
                name=record["p"]["providerName"]
            ))
        ctr=ctr+1
    return responses.Response(
        metadata=schemas.Metadata(
            currentPage=skip/limit,
            pageSize=limit,
            totalCount=ctr,
            totalPages=math.ceil(ctr/limit)
        ),
        result=results
    )

def get_all_categories(skip: int, limit: int):
    db_categories = models.ServiceCategory.match_nodes()
    results = []
    ctr=0
    for idx, db_category in enumerate(db_categories):
        if (idx>=skip and idx<limit+skip):
            results.append(schemas.ServiceCategory(
                name=db_category.name,
                # description=db_category.description
            ))
        ctr=ctr+1
    return responses.Response(
        metadata=schemas.Metadata(
            currentPage=skip/limit,
            pageSize=limit,
            totalCount=ctr,
            totalPages=math.ceil(ctr/limit)
        ),
        result=results
    )

def check_membership(user_id: str, provider: str):
    cypher=f"""
    MATCH (u:USER)-[m:IS_MEMBER]->(p:ServiceProvider)
    WHERE u.id=$user_id AND p.providerAbbr=$provider
    RETURN m
    """
    params={
        "user_id": user_id,
        "provider": provider
    }
    graph=GraphConnection()
    return not graph.cypher_read(cypher, params)==None

def create_measurement(user_id, service: str, measurement: schemas.Measurement):
    if measurement.value < 0:
        return None
    
    db_service = models.Service.match(service)
    if db_service is None:
        return None
    cypher=f"""
    MATCH (p:ServiceProvider)-->(s:SERVICE)
    WHERE s.abbreviation=$service
    RETURN p
    """
    params = {
        "service": service
    }
    graph = GraphConnection()
    provider=graph.cypher_read_many(cypher, params)[0]["p"]
    db_kpi = models.KPI.match(measurement.kpi)
    if not check_membership(user_id, provider=provider["providerAbbr"]):
        return None
    if db_kpi is None:
        return None    
    date = measurement.date+"-01T00:00:00Z" if len(measurement.date)==7 else measurement.date+"T00:00:00Z"
    point = (
        Point(provider["providerAbbr"]).tag("service", service).field(measurement.kpi, measurement.value).time(date,"s")
    )
    write_api.write(bucket=bucket, org=org, record=point)
    return measurement

def find_indicators(skip: int, limit: int, category: str|None, service: str|None):
    db_indicators = models.KPI.match_nodes()
    graph=GraphConnection()
    
    cypher_service=f"""
    MATCH (s:SERVICE)-[d:DEFINES]->(k:KPI)
    WHERE s.abbreviation=$service
    RETURN *
    """
    params_service={
        "service": service
    }
    service_kpis=graph.cypher_read_many(cypher_service, params_service)
    
    if(service):
        cypher=f"""
        MATCH (s:SERVICE)-[:OF_CATEGORY]->(c:CATEGORY)
        WHERE s.abbreviation=$service
        RETURN c
        """
        params={
            "service": service
        }
        category=graph.cypher_read(cypher,params)["c"]["name"]
        db_categories = [models.ServiceCategory.match(category)]
    elif(category):
        db_categories = [models.ServiceCategory.match(category)]
    else: 
        db_categories = models.ServiceCategory.match_nodes()
    
    results = []
    ctr = 0
    db_indicators.sort(key=lambda x: x.name)
    for idx, db_indicator in enumerate(db_indicators):
        if (idx>=skip and idx<limit+skip):
            categories=[]
            selected = False
            for db_category in db_categories:
                cypher=f"""
                MATCH (c:CATEGORY)-[d:DEFINES]->(k:KPI)
                WHERE c.name=$category AND k.name=$indicator
                RETURN *
                """
                params={
                    "category": db_category.name,
                    "indicator": db_indicator.name
                }
                record=graph.cypher_read(cypher,params)
                if (record):
                    categories.append(schemas.CategoryNecessity(name=record["c"]["name"], necessity=record["d"]["necessity"]))
                    selected=True
                else:
                    categories.append(schemas.CategoryNecessity(name=db_category.name, necessity=None))
            for service_kpi in service_kpis:
                if (db_indicator.name==service_kpi["k"]["name"]):
                    selected=True
            results.append(schemas.KPI(
                name=db_indicator.name,
                description=db_indicator.description,
                categories=categories,
                selected=selected
            ))
        ctr=ctr+1
    
    return responses.Response(
        metadata=schemas.Metadata(
            currentPage=skip/limit,
            pageSize=limit,
            totalCount=ctr,
            totalPages=math.ceil(ctr/limit)
        ),
        result=results
    )

def get_measurements_for_service(service: str, indicator_list: list[str], start: str, stop: str, page: int, pageSize: int):
    query="""
    from(bucket: "kpis")
    |> range(start: time(v: "{start}"), stop: time(v: "{stop}"))
    |> filter(fn: (r) => r["service"] == "{service}")
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    """.format(start=start, stop=stop, service=service)
    
    results=[]
    print(results)
    tables = query_api.query(query=query, org="scorpion")
    skip = page*pageSize
    limit = page*pageSize+pageSize
    for table in tables:
        for record in table.records[skip:limit]:
            for i in range(7,len(table.columns)):
                if (record[table.columns[i].label] and (len(indicator_list)==0 or table.columns[i].label in indicator_list)):
                    results.append(schemas.Measurement(date=str(record["_time"]), kpi=table.columns[i].label, value=record[table.columns[i].label]))
    metadata=schemas.Metadata(
        currentPage=page,
        pageSize=pageSize,
        totalCount=len(tables[0].records) if len(tables)>0 else 0,
        totalPages=math.ceil(len(tables[0].records)/pageSize) if len(tables)>0 else 0
    )
    print(results)
    return responses.Response(
        metadata=metadata,
        result=results
    )

def get_all_services(skip: int, limit: int, provider: str|None, service: str|None):
    cypher = f"""
    MATCH (c:CATEGORY)<-[:OF_CATEGORY]-(s:SERVICE)<-[:HAS_SERVICES]-(p:ServiceProvider)
    WHERE (p.providerAbbr in split($provider,',') or $provider is null) AND (s.abbreviation=$service or $service is null)
    WITH *
    OPTIONAL MATCH (s)-[:PROVIDED_IN]->(consort:CONSORTIA)
    RETURN s {{.name, .abbreviation, .license, .stage}},c {{.name}},p {{.providerAbbr, .providerName}}, collect(consort.name) as consortia
    """
    params={
        "provider": provider, 
        "service": service
    }
    ic(params)
    graph = GraphConnection()
    records = graph.cypher_read_many(cypher, params)
    
    ic(records)

    # for record in records:
    #     # ic(record["s"])
    #     try:
    #         ic(models.Service.parse_obj(record["s"]))
    #     except ValidationError as e:
    #         ic(repr(e.errors()[0]))
    
    # db_results = []
    db_results = [{
        "service": models.Service.parse_obj(record["s"]), 
        "category": models.ServiceCategory.parse_obj(record["c"]),
        "provider": models.ServiceProvider.parse_obj(record["p"]),
        "consortia": record["consortia"]
    } for record in records]
    results = []
    ctr = 0
    for idx, db_result in enumerate(db_results):
        # ic(db_result)
        if (idx>=skip and idx<skip+limit):
            results.append(schemas.Service(
                abbreviation=db_result["service"].abbreviation,
                name=db_result["service"].name,
                category=db_result["category"].name,
                provider=db_result["provider"].providerAbbr,
                license=db_result["service"].license,
                consortia=db_result["consortia"],
                stage=db_result["service"].stage
            ))
        ctr=ctr+1
    return responses.Response(
        metadata=schemas.Metadata(
            currentPage=skip/limit,
            pageSize=limit,
            totalCount=ctr,
            totalPages=math.ceil(ctr/limit)    
        ),
        result=results
    )