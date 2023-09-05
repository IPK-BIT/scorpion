import bcrypt
from neontology import GraphConnection
from sqlalchemy.orm import Session
from uuid import uuid4

from routers.aai.utils import models, schemas
from utils import models as neo_models
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email==email).first()

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.user_name==name).first()

def get_open_requests(db: Session):
    return db.query(models.User).filter(models.User.accepted==False).all()

def create_user(db: Session, user: schemas.UserCreate):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.password.encode("utf8"), salt)
    db_user = models.User(
        user_id=str(uuid4()),
        user_name=user.user_name,
        email=user.email,
        salt=salt,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return schemas.User(
        user_id=db_user.user_id,
        user_name=db_user.user_name,
        email=db_user.email
    )
    
def finish_registration(db: Session, user_id: str, is_admin: bool, accept: bool):
    db_user:models.User = db.query(models.User).filter(models.User.user_id==user_id).first()
    if accept:
        db_user.is_admin=is_admin
        db_user.accepted=True
        db.commit()
        return schemas.User(
            user_id=db_user.user_id,
            user_name=db_user.user_name,
            email=db_user.email
        )
    else:
        db.delete(db_user)
        db.commit()
        return schemas.User(
            user_id=user_id,
            user_name="request declined",
            email="request declined"
        )

def get_user_memberships_by_id(user_id: str):
    cypher=f"""
    MATCH (u:USER)-[:IS_MEMBER]->(p:ServiceProvider)
    WHERE u.id=$user_id
    RETURN *
    """
    params={"user_id": user_id}
    graph = GraphConnection()
    results = []
    records = graph.cypher_read_many(cypher, params)
    for record in records:
        results.append(record["p"]["providerAbbr"])
    return results
    

def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.user_id==user_id).first()

def is_valid_email(email: str):
    return email.count("@") == 1 and email.count(".") == 1

def get_users(db: Session):
    return db.query(models.User).filter(models.User.accepted==True).all()

################################REQUESTS################################

def create_request(db: Session, user: schemas.User, providers: str):
    db_request = models.Request(
        request_id=str(uuid4()),
        user_id=user.user_id,
        providers=providers
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)    
    return schemas.Request(
        id=db_request.request_id,
        mail=user.email,
        username=user.user_name,
        provider=providers
    )
    
def get_requests(db: Session, user_id: str):
    results = []
    if get_user_by_id(db, user_id).is_admin:
        results = db.query(models.Request).all()
    else:
        results = db.query(models.Request).filter(models.Request.user_id==user_id).all()
    return results

def remove_request(db: Session, request_id: str, accept: bool):
    db_request:models.Request = db.query(models.Request).filter(models.Request.request_id==request_id).first()
    db_user:models.User=get_user_by_id(db, db_request.user_id)
    
    if accept:
        neo_user = neo_models.User.match(db_user.user_id)
        if not neo_user:
            neo_user: neo_models.User = neo_models.User(
                id=db_user.user_id
            )
            neo_user.create()
        providers = db_request.providers.split(',')
        for provider in providers:
            neo_provider = neo_models.ServiceProvider.match(provider)
            is_member=neo_models.IsMember(
                source=neo_user,
                target=neo_provider
            )
            is_member.merge()
        
    
    db.delete(db_request)
    db.commit()
    
    return schemas.Request(
        id=db_request.request_id,
        mail=db_user.email,
        username=db_user.user_name,
        provider=db_request.providers
    )
    
def update_user(db: Session, user: schemas.UserDetail):
    db_user: models.User = db.query(models.User).filter(models.User.user_name==user.user_name).first()
    db_user.is_admin=user.is_admin
    
    remove_providers = []
    cypher=f"""
    MATCH (u:USER)-[:IS_MEMBER]->(p:ServiceProvider)
    WHERE u.id=$user_id
    RETURN *
    """
    params={
        "user_id": db_user.user_id
    }
    graph=GraphConnection()
    records = graph.cypher_read_many(cypher, params)
    for record in records:
        if not record["p"]["providerAbbr"] in user.providers:
            remove_providers.append(record["p"]["providerAbbr"])
            
    for provider in remove_providers:
        cypher=f"""
        MATCH (u:USER)-[m:IS_MEMBER]->(p:ServiceProvider)
        WHERE u.id=$user_id AND p.providerAbbr=$provider
        DELETE m
        """
        params={
            "user_id": db_user.user_id,
            "provider": provider
        }
        graph.cypher_write(cypher, params)
    
    providers = []
    cypher=f"""
    MATCH (u:USER)-[:IS_MEMBER]->(p:ServiceProvider)
    WHERE u.id=$user_id
    RETURN *
    """
    params={
        "user_id": db_user.user_id
    }
    graph=GraphConnection()
    records = graph.cypher_read_many(cypher, params)
    for record in records:
        providers.append(record["p"]["providerAbbr"])
    user.providers=providers
    
    db.commit()
    
    return user

def remove_user(db: Session, user_name: str):
    db_user:models.User=db.query(models.User).filter(models.User.user_name==user_name).first()
    providers = []
    cypher=f"""
    MATCH (u:USER)-[:IS_MEMBER]->(p:ServiceProvider)
    WHERE u.id=$user_id
    RETURN *
    """
    params={
        "user_id": db_user.user_id
    }
    graph=GraphConnection()
    records = graph.cypher_read_many(cypher, params)
    for record in records:
        providers.append(record["p"]["providerAbbr"])
    
    user=schemas.UserDetail(
        user_name=user_name,
        email=db_user.email,
        is_admin=db_user.is_admin,
        providers=providers
    )
    cypher=f"""
    MATCH (u:USER)-[m:IS_MEMBER]->(:ServiceProvider)
    WHERE u.id=$user_id
    DELETE m
    """
    params={
        "user_id": db_user.user_id
    }
    graph.cypher_write(cypher, params)
    
    db_requests=db.query(models.Request).filter(models.Request.user_id==db_user.user_id).all()
    for db_request in db_requests:
        db.delete(db_request)
    
    db.delete(db_user)
    db.commit()
    
    return user