from fastapi import APIRouter
from icecream import ic
from utils import models, schemas, responses
from routers.internal.util import crud
from dotenv import load_dotenv
import os

load_dotenv()
prefix = os.getenv("PREFIX")

router = APIRouter(
    prefix=f"{prefix}/api/v1",
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

@router.delete('/measurements', response_model=responses.Response[schemas.Measurement])
async def delete_measurements(service: str, start: str, stop: str):
    return crud.delete_measurements(service, start, stop)

@router.get('/notification')
async def get_notifications():
    return 'We just released Version 2 of the Web Interface. If you encounter any introduced bugs, please report them <a class="underline" href="https://github.com/IPK-BIT/scorpion/issues">here</a>.'