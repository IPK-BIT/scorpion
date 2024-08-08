from icecream import ic
from neontology import GraphConnection
from uuid import uuid4
import json

from utils import models, schemas
from utils.influx import bucket, org, delete_api
from routers.external.util.crud import get_measurements_for_service

def create_provider(provider: schemas.ServiceProvider):
    dupl = models.ServiceProvider.match(provider.abbreviation)
    if not dupl is None:
        return None
    
    db_provider = models.ServiceProvider(
        providerAbbr = provider.abbreviation,
        providerName = provider.name
    )
    db_provider.create()
    
    return provider

def create_service(service: schemas.Bonsai):
    dupl = models.Service.match(service.abbreviation)
    if not dupl is None:
        print("Service already exists!")
        return None
    db_provider = models.ServiceProvider.match(service.provider)
    if db_provider is None:
        print("Provider not found!")
        return None
    db_category = models.ServiceCategory.match(service.category)
    if db_category is None:
        print("Category not found!")
        return None
    db_consortia = []
    graph = GraphConnection()
    for consortium in service.consortia:
        db_consortia.append(models.Consortia.parse_obj(graph.cypher_read(f"""MATCH (c:CONSORTIA) WHERE c.name=$consortium RETURN c {{ .name }}""", {"consortium": consortium})['c']))
        # db_consortia.append(models.Consortia.match(consortium))
        
    
    db_service = models.Service(
        abbreviation=service.abbreviation,
        name=service.name,
        license=service.license,
        stage=service.stage,
        # description=service.description,
        # areaofapplication=json.dumps(service.areaofapplication.json()),
        # inputformats=service.inputformats,
        # outputformats=service.outputformats,
        # developmentstage=service.developmentstage,
        # version=service.version,
        # documentation=service.documentation,
        # license=service.license,
        # link=service.link,
        # serviceorientation=service.serviceorientation,
        # includeincataglog=service.includeincataglog,
        # serviceprovidedas=json.dumps(service.serviceprovidedas.json()),
        # funding=service.funding,
        # contact=service.contact,
        # helpdesk=service.helpdesk,
        # supporteduntil=service.supporteduntil,
        # technicalbackbone=service.technicalbackbone,
        # disasterplan=service.disasterplan,
        # entrancecontrol=service.entrancecontrol,
        # operationstability=service.operationstability,
        # templates=service.templates,
        # communication=service.communication,
        # registered=json.dumps(service.registered.json()),
        # publications=service.publications
    )
    db_service.create()
    has_service = models.HasServices(
        source=db_provider,
        target=db_service
    )
    has_service.merge()
    of_category = models.OfCategory(
        source=db_service,
        target=db_category
    )
    of_category.merge()
    for kpi in service.additionalKPI:
        db_kpi = models.KPI.match(kpi.name)
        defines = models.Defines(
            source=db_service,
            target=db_kpi,
            necessity="optional"
        )
        defines.merge()
    print(db_consortia)
    for consortium in db_consortia:
        provided_in = models.ProvidedIn(
            source=db_service,
            target=consortium
        )
        provided_in.merge()
    return service

def create_category(category: schemas.ServiceCategory):
    dupl = models.ServiceCategory.match(category.name)
    if not dupl is None:
        return None
    db_category = models.ServiceCategory(
        name=category.name
    )
    db_category.create()
    return category

def create_kpi(kpi: schemas.KPI):
    cypher=f"""
    MATCH (k:KPI)
    WHERE k.name=$kpi
    RETURN k
    """
    params={"kpi": kpi.name}
    graph = GraphConnection()
    dupl = graph.cypher_read(cypher, params)
    if not dupl is None:
        return None
    db_kpi = models.KPI(
        name=kpi.name,
        description=kpi.description
    )
    db_kpi.create()
    return kpi

def delete_measurements(service: str, start: str, stop: str):
    ic(start,stop)
    response = get_measurements_for_service(service, [], start, stop, 0, 100)
    ic(response)
    delete_api.delete(start, stop, predicate='service="'+service+'"', bucket=bucket, org=org)
    print(response)
    return response