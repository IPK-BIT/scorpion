import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from neontology import init_neontology
from icecream import ic

from utils import sqlite_database
# from utils.jwt_utils import JWTBearer, verify_jwt
from utils.jwt_utils import verify_jwt, jwt_or_key_auth
from routers.aai import aai
from routers.aai.utils import models as aai_models
from routers.external import external
from routers.internal import internal

aai_models.Base.metadata.create_all(bind=sqlite_database.engine)
load_dotenv()

prefix=os.getenv("PREFIX")

app = FastAPI(
    title="ScorPIoN API",
    version="0.1.0",
    openapi_url=f"{prefix}/api/v1/openapi.json",
    docs_url=f"{prefix}/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup_event():
    init_neontology()

@app.get("/", response_class=RedirectResponse, include_in_schema=False)
def redirect_docs():
    return "http://localhost:8000/docs"     

app.include_router(aai.router)
app.include_router(internal.router, dependencies=[Depends(jwt_or_key_auth)])
app.include_router(external.router, dependencies=[Depends(jwt_or_key_auth)])