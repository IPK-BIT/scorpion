from neontology import BaseNode, BaseRelationship

class Service(BaseNode):
    
    __primaryproperty__="abbreviation"
    __primarylabel__="SERVICE"
    
    name: str
    abbreviation: str
    stage: str
    license: str
    # areaofapplication: str|None
    # description: str|None
    # inputformats: str|None
    # outputformats: str|None
    # developmentstage: str|None
    # version: str|None
    # documentation: str|None
    # license: str|None
    # link: str|None
    # serviceorientation: str|None
    # includeincataglog: str|None
    # serviceprovidedas: str|None
    # funding: str|None
    # contact: str|None
    # helpdesk: str|None
    # supporteduntil: str|None
    # technicalbackbone: str|None
    # disasterplan: str|None
    # entrancecontrol: str|None
    # operationstability: str|None
    # templates: str|None
    # communication: str|None
    # registered: str|None
    # publications: str|None
    
    class Config:
        extra = "allow"

class User(BaseNode):
    __primaryproperty__="id"
    __primarylabel__="USER"
    
    id: str
    admin: bool
    username: str
    email: str

class Token(BaseNode):
    __primaryproperty__="value"
    __primarylabel__="TOKEN"

    value: str
    name: str

class ServiceCategory(BaseNode):
    __primaryproperty__="name"
    __primarylabel__="CATEGORY"
    
    name: str
    # description: str|None

class ServiceProvider(BaseNode):
    __primaryproperty__="providerAbbr"
    __primarylabel__="ServiceProvider"
    
    providerAbbr: str
    providerName: str

class Consortia(BaseNode):
    __primaryproperty__="name"
    __primarylabel__="CONSORTIA"
    
    name: str

class KPI(BaseNode):
    __primaryproperty__="name"
    __primarylabel__="KPI"
    
    name: str
    description: str|None

class Measurement(BaseNode):
    __primaryproperty__="measurementId"
    __primarylabel__="Measurement"
    
    measurementId: str
    value: int
    comment: str|None
    date: str
    
class HasToken(BaseRelationship):
    __relationshiptype__='HAS_TOKEN'

    source: User
    target: Token

class IsMember(BaseRelationship):
    __relationshiptype__="IS_MEMBER"
    
    source: User
    target: ServiceProvider
    id: str
    approved: int

class HasServices(BaseRelationship):
    __relationshiptype__="HAS_SERVICES"
    
    source: ServiceProvider
    target: Service

class OfCategory(BaseRelationship):
    __relationshiptype__="OF_CATEGORY"
    
    source: Service
    target: ServiceCategory

class HasMeasurements(BaseRelationship):
    __relationshiptype__="HAS_MEASUREMENTS"
    
    source: Service
    target: Measurement

class HasKPIs(BaseRelationship):
    __relationshiptype__="HAS_KPIS"
    
    source: ServiceCategory
    target: KPI

class OfType(BaseRelationship):
    __relationshiptype__="OF_TYPE"
    
    source: Measurement
    target: KPI

class Defines(BaseRelationship):
    __relationshiptype__="DEFINES"
    
    source: ServiceCategory|Service
    target: KPI
    necessity: str

class ProvidedIn(BaseRelationship):
    __relationshiptype__="PROVIDED_IN"
    
    source: Service
    target: Consortia