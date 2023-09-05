from fastapi import APIRouter
from icecream import ic
from utils import models, schemas
from routers.internal.util import crud

router = APIRouter(
    prefix="/api/v1",
    tags=["Internal Endpoints"],
    include_in_schema=False
)


@router.post("/providers", response_model=list[schemas.ServiceProvider]
)
async def create_providers(
    providers: list[schemas.ServiceProvider]|schemas.ServiceProvider
):
    results = []
    if isinstance(providers, list):
        for provider in providers:
            result = crud.create_provider(provider)
            if not result is None:
                results.append(result)
    else: 
        result = crud.create_provider(providers)
        if not result is None:
            results.append(result)
    return results

@router.post("/categories", response_model=list[schemas.ServiceCategory]|schemas.ServiceCategory
)
async def create_categories(
    categories: list[schemas.ServiceCategory]|schemas.ServiceCategory
):    
    results = []
    if isinstance(categories, list):
        for category in categories:
            result = crud.create_category(category)
            if not result is None:
                results.append(result)
    else: 
        result = crud.create_category(categories)
        if not result is None:
            results.append(result)
    return results

@router.post("/indicators", response_model=list[schemas.KPI]|schemas.KPI)
async def create_kpis(
    kpis: list[schemas.KPI]|schemas.KPI
):    
    results = []
    if isinstance(kpis, list):
        for kpi in kpis:
            result = crud.create_kpi(kpi)
            if not result is None:
                results.append(result)
    else: 
        result = crud.create_kpi(kpis)
        if not result is None:
            results.append(result)
    return results

@router.post('/bonsai')
async def create_service(service: schemas.Bonsai):
    result = crud.create_service(service)
    return result

@router.delete('/measurements', response_model=schemas.MeasurementResponse)
async def delete_measurements(service: str, start: str, stop: str):
    return crud.delete_measurements(service, start, stop)