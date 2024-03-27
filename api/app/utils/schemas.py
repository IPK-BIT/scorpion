from pydantic import BaseModel

class ServiceProvider(BaseModel):
    abbreviation: str
    name: str

class Service(BaseModel):
    abbreviation: str
    name: str
    category: str
    provider: str|None

class Measurement(BaseModel):
    kpi: str
    date: str
    value: int
    # comment: str|None
    
class Metadata(BaseModel):
    currentPage: int
    pageSize: int
    totalPages: int
    totalCount: int
    
class MeasurementResponse(BaseModel):
    metadata: Metadata
    results: list[Measurement]

class ServiceCategory(BaseModel):
    name: str

class CategoryNecessity(BaseModel):
    name: str
    necessity: str|None

class KPI(BaseModel):
    name: str
    description: str
    categories: list[CategoryNecessity]
    selected: bool|None
    
class IndicatorResponse(BaseModel):
    category: list[KPI]
    others: list[KPI]

class ServiceArea(BaseModel):
    planning: bool
    harmonization: bool
    access: bool
    discover: bool
    processing: bool
    support: bool

class PartOf(BaseModel):
    partOf: bool
    percentage: int

class ServicePartOf(BaseModel):
    institutionalMission: PartOf
    projectFunding: PartOf
    others: PartOf

class Registration(BaseModel):
    registered: bool
    url: str

class ServiceRegistration(BaseModel):
    biotools: Registration
    risources: Registration
    fairsharing: Registration
    re3data: Registration
    others: Registration

class Bonsai(BaseModel):
    name: str
    abbreviation: str
    provider: str
    areaofapplication: ServiceArea|None
    description: str|None
    inputformats: str|None
    outputformats: str|None
    developmentstage: str|None
    version: str|None
    documentation: str|None
    license: str|None
    link: str|None
    serviceorientation: str|None
    includeincataglog: str|None
    serviceprovidedas: ServicePartOf|None
    funding: str|None
    contact: str|None
    helpdesk: str|None
    supporteduntil: str|None
    technicalbackbone: str|None
    disasterplan: str|None
    entrancecontrol: str|None
    operationstability: str|None
    templates: str|None
    communication: str|None
    registered: ServiceRegistration|None
    publications: str|None
    category: str
    additionalKPI: list[KPI]