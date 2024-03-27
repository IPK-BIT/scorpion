from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials
from typing import Annotated
from icecream import ic
from utils import models, schemas, jwt_utils, responses
from routers.external.util import crud

async def common_parameters(page: Annotated[int|None, Query(ge=0)] = None, pageSize: Annotated[int|None, Query(gt=0)] = None):
    return {"page": page, "pageSize": pageSize}

CommonDeps = Annotated[dict, Depends(common_parameters)]

router = APIRouter(
    prefix="/api/v1",
    tags=["Public Endpoints"]
)

@router.get("/providers", response_model=responses.Response[schemas.ServiceProvider])
async def list_providers(commons: CommonDeps, token: dict = Depends(jwt_utils.verify_jwt), is_member: bool|None = None):
    page = commons["page"] if commons["page"]!=None else 0
    pageSize = commons["pageSize"] if commons["pageSize"]!=None else 100
    skip = page*pageSize
    limit = pageSize
    if (is_member):
        return crud.get_providers_by_user(token["sub"], skip, limit)
    return crud.get_all_providers(skip, limit)

@router.get("/categories", response_model=responses.Response[schemas.ServiceCategory])
async def list_categories(commons: CommonDeps):
    page = commons["page"] if commons["page"]!=None else 0
    pageSize = commons["pageSize"] if commons["pageSize"]!=None else 100
    skip = page*pageSize
    limit = pageSize
    return crud.get_all_categories(skip, limit)

@router.get('/indicators', response_model=responses.Response[schemas.KPI])
async def list_indicators(commons: CommonDeps, category: str|None = None, service: str|None = None):
    page = commons["page"] if commons["page"]!=None else 0
    pageSize = commons["pageSize"] if commons["pageSize"]!=None else 100
    skip = page*pageSize
    limit = pageSize
    return crud.find_indicators(skip, limit, category, service)

@router.get("/services", response_model=responses.Response[schemas.Service])
async def list_services(commons: CommonDeps, provider: str|None = None, service: str|None = None):
    page = commons["page"] if commons["page"]!=None else 0
    pageSize = commons["pageSize"] if commons["pageSize"]!=None else 100
    skip = page*pageSize
    limit = pageSize
    return crud.get_all_services(skip, limit, provider, service)

@router.get('/measurements', response_model=responses.Response[schemas.Measurement])
async def list_measurements(commons: CommonDeps, service: str, indicators: str|None = None, start: str = "2022-01-01T00:00:00Z", stop: str = "2030-12-31T00:00:00Z"):
    page = commons["page"] if commons["page"]!=None else 0
    pageSize = commons["pageSize"] if commons["pageSize"]!=None else 100
    if not indicators: 
        indicator_list = []
    else: 
        indicator_list = indicators.split(',')
    return crud.get_measurements_for_service(service, indicator_list, start, stop, page, pageSize)

@router.post("/measurements", response_model=list[schemas.Measurement]|schemas.Measurement)
async def create_measurements(
    service: str,
    measurements: list[schemas.Measurement]|schemas.Measurement,
    token: dict = Depends(jwt_utils.verify_jwt)
):
    user_id=token['sub']
    results = []
    if isinstance(measurements, list):
        for measurement in measurements:
            result = crud.create_measurement(user_id, service, measurement)
            if not result is None:
                results.append(result)
    else: 
        result = crud.create_measurement(user_id, service, measurements)
        if not result is None:
            results.append(result)
    return results