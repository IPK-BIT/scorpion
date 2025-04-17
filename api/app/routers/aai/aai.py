from fastapi import APIRouter, Depends, HTTPException, status, Response
from neontology import GraphConnection
from uuid import uuid4
import requests

from icecream import ic

import os
from dotenv import load_dotenv

from utils.jwt_utils import jwt_or_key_auth
from utils import models as neo_models
from routers.aai.utils import schemas

load_dotenv()
prefix = os.getenv('PREFIX')

router = APIRouter(
    prefix=f"{prefix}/aai",
    tags=["AAI"]
)

async def get_admin_access_token():
    basic_auth = os.getenv('KEYCLOAK_BASIC_AUTH')
    url = 'https://scorpion.bi.denbi.de/realms/master/protocol/openid-connect/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {basic_auth}'
    }
    data = {
        'username': 'register',
        'password': 'register',
        'grant_type': 'password'
    }

    token_response = requests.post(url, headers=headers, data=data)
    token_response.raise_for_status()
    token = token_response.json()['access_token']
    return token

async def check_admin_role(current_user, token):
    response = requests.get(f"https://scorpion.bi.denbi.de/admin/realms/scorpion/users/{current_user['sub']}/role-mappings", headers={'Authorization': f'Bearer {token}'})
    response.raise_for_status()
    role_mappings = response.json()
    is_admin = False
    for role_mapping in role_mappings['realmMappings']:
        if role_mapping['name'] == 'admin':
            is_admin = True
            break
    return is_admin

def read_providers_by_user(user_id):
    graph=GraphConnection()
    cypher=f"""
        MATCH (:USER {{id: $user_id}})-[:IS_MEMBER {{approved: 1}}]->(p:ServiceProvider)
        RETURN collect(p.providerAbbr) as p
        """
    params = {
        "user_id": user_id
    }
    providers = graph.cypher_read(cypher, params)['p']
    return providers

@router.post('/register')
async def register(user: schemas.UserCreate):    
    token = await get_admin_access_token()
    
    response = requests.get(f"https://scorpion.bi.denbi.de/admin/realms/scorpion/users?username={user.user_name}", headers={'Authorization': f'Bearer {token}'})
    response.raise_for_status()
    if (len(response.json()) > 0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already registered"
        )    
    
    response = requests.get(f"https://scorpion.bi.denbi.de/admin/realms/scorpion/users?email={user.email}", headers={'Authorization': f'Bearer {token}'})
    response.raise_for_status()
    if (len(response.json()) > 0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        ) 
    
    response = requests.post('https://scorpion.bi.denbi.de/admin/realms/scorpion/users', headers={'Authorization': f'Bearer {token}'}, json={
        "username": user.user_name,
        "email": user.email,
        "enabled": False,
    })
    response.raise_for_status()
    
    response = requests.get(f"https://scorpion.bi.denbi.de/admin/realms/scorpion/users?username={user.user_name}", headers={'Authorization': f'Bearer {token}'})
    response.raise_for_status()
    
    user_id = response.json()[0]['id']
    
    response = requests.put(f"https://scorpion.bi.denbi.de/admin/realms/scorpion/users/{user_id}/reset-password", headers={'Authorization': f'Bearer {token}'}, json={
        "type": "password",
        "temporary": False,
        "value": user.password 
    })
    response.raise_for_status()   
    
    return #response.json()

@router.get('/requests/registration', include_in_schema=False, response_model=list[schemas.User])
async def get_open_registrations(jwt: dict = Depends(jwt_or_key_auth)):
    # token = await get_admin_access_token()
    
    # kc_response = requests.get(f"https://scorpion.bi.denbi.de/admin/realms/scorpion/users?enabled=false", headers={'Authorization': f'Bearer {token}'})
    # kc_response.raise_for_status()
    # users = kc_response.json()

    # response = []
    # for user in users:
    #     response.append(schemas.User(
    #         user_id=user['id'],
    #         email=user['email'],
    #         user_name=user['username']
    #     ))
    # return response
    return []

@router.delete('/requests/registration', include_in_schema=False)#, response_model=schemas.User)
async def remove_registration_request(request_id:str, is_admin: bool, accept: bool, response: Response, jwt: dict = Depends(jwt_or_key_auth)):
    token = await get_admin_access_token()
    if await check_admin_role(jwt, token):
        if accept:
            response = requests.put(f"https://scorpion.bi.denbi.de/admin/realms/scorpion/users/{request_id}", headers={'Authorization': f'Bearer {token}'}, json={
                "enabled": True
            })
            response.raise_for_status()
            neo_user = neo_models.User.match(request_id)
            if not neo_user:
                neo_user = neo_models.User(id=request_id)
                neo_user.create()
            if is_admin:
                roles_response = requests.get(f"https://scorpion.bi.denbi.de/admin/realms/scorpion/roles", headers={'Authorization': f'Bearer {token}'})
                roles_response.raise_for_status()
                roles = roles_response.json()
                admin_role = next((role for role in roles if role['name'] == 'admin'), None)
                ic(admin_role)
                response = requests.post(f"https://scorpion.bi.denbi.de/admin/realms/scorpion/users/{request_id}/role-mappings/realm", headers={'Authorization': f'Bearer {token}'}, json=[
                    admin_role
                ])
                response.raise_for_status()
            #TODO: set api reader role
        else:
            response = requests.delete(f"https://scorpion.bi.denbi.de/admin/realms/scorpion/users/{request_id}", headers={'Authorization': f'Bearer {token}'})
            response.raise_for_status()
    else:
        response.status_code=status.HTTP_403_FORBIDDEN
    return None

@router.get('/details', response_model=schemas.UserDetail)
async def get_user(current_user: dict = Depends(jwt_or_key_auth)):
    neo_user = neo_models.User.match(current_user['sub'])
    if not neo_user:
        first_user = len(neo_models.User.match_nodes())==0
        neo_user = neo_models.User(id=current_user['sub'], admin=first_user, username=current_user['preferred_username'], email=current_user['email'])
        neo_user.create()
    return schemas.UserDetail(
        user_name=neo_user.username,
        email=neo_user.email,
        is_admin=neo_user.admin,
        providers=read_providers_by_user(current_user['sub'])
    )
    
@router.post('/requests/membership', response_model=schemas.Request, status_code=status.HTTP_201_CREATED)
def request_membership(providers: str, jwt: dict = Depends(jwt_or_key_auth)):
    neo_user = neo_models.User.match(jwt['sub'])
    neo_provider = neo_models.ServiceProvider.match(providers)
    request_id = uuid4().hex
    is_member = neo_models.IsMember(
        id=request_id,
        source=neo_user, 
        target=neo_provider, 
        approved=0
    )
    is_member.merge()
    
    return schemas.Request(
        id=request_id,
        mail=jwt['email'],
        username=jwt['preferred_username'],
        provider=providers
    )

@router.get('/requests/membership', response_model=list[schemas.Request], include_in_schema=False)
async def get_membership_requests(jwt: dict = Depends(jwt_or_key_auth)):
    cypher = f"""
    MATCH (u:USER)-[m:IS_MEMBER {{approved: 0}}]->(p:ServiceProvider) 
    RETURN *
    """
    graph=GraphConnection()
    results = graph.cypher_read_many(cypher)
    # token = await get_admin_access_token()
    # kc_response = requests.get(f"https://scorpion.bi.denbi.de/admin/realms/scorpion/users?enabled=True", headers={'Authorization': f'Bearer {token}'})
    # kc_response.raise_for_status()
    # users = kc_response.json()
    member_requests=[]
    for result in results:
        # user = next((user for user in users if user['id'] == result['u']['id']), None)
        member_requests.append(schemas.Request(
            id=result['m']['id'],
            # mail=jwt['email'],
            # username=jwt['username'],
            mail=result['u']['email'],
            username=result['u']['username'],
            provider=result['p']['providerAbbr']
        ))
    return member_requests

@router.delete('/requests/membership', response_model=schemas.Request|None, include_in_schema=False)
async def remove_membership_request(request_id:str, accept: bool, response: Response, jwt: dict = Depends(jwt_or_key_auth)):    
    neo_user = neo_models.User.match(jwt['sub'])    
    if neo_user.admin:
        graph = GraphConnection()
        if accept:
            cypher = f"""
            MATCH (:USER)-[m:IS_MEMBER {{id: '{request_id}'}}]->(:ServiceProvider)
            SET m.approved = 1
            """
        else:
            cypher = f"""
            MATCH (:USER)-[m:IS_MEMBER {{id: '{request_id}'}}]->(:ServiceProvider)
            DELETE m
            """
        params = {
            "request_id": request_id
        }
        graph.cypher_write(cypher, params)
    else:
        response.status_code=status.HTTP_403_FORBIDDEN
    return
    
@router.get('/users', response_model=list[schemas.UserDetail], include_in_schema=False)
async def list_all_users(jwt: dict = Depends(jwt_or_key_auth)):
    # token = await get_admin_access_token()
    # kc_response = requests.get(f"https://scorpion.bi.denbi.de/admin/realms/scorpion/users?enabled=True", headers={'Authorization': f'Bearer {token}'})
    # kc_response.raise_for_status()
    # users = kc_response.json()
    # results = []
    # for user in users:
    #     if not 'service-account' in user['username']:
    #         is_admin = await check_admin_role({'sub': user['id']}, token)
            
    #         providers = read_providers_by_user(user['id'])
            
    #         results.append(schemas.UserDetail(
    #             user_id=user['id'],
    #             email=user['email'],
    #             user_name=user['username'],
    #             is_admin=is_admin,
    #             providers=providers
    #         ))
    user = neo_models.User.match(jwt['sub'])
    if not user.admin:
        return []
    neo_users = neo_models.User.match_nodes()
    results = []
    for user in neo_users:
        results.append(schemas.UserDetail(
            user_name=user.username,
            # email=user.email,
            email=user.email,
            is_admin=user.admin,
            providers=read_providers_by_user(user.id)
        ))
    return results

@router.put('/users', response_model=schemas.UserDetail, include_in_schema=False)
async def update_user(user: schemas.UserDetail, response: Response, jwt: dict = Depends(jwt_or_key_auth)):  
    jwt_user = neo_models.User.match(jwt['sub'])
    if not jwt_user.admin:
        return {}
    
    graph = GraphConnection()
    cypher = f"""
    MATCH (u:USER {{username: $user_name}})
    OPTIONAL MATCH (u)-[:IS_MEMBER]->(p:ServiceProvider)
    RETURN u, collect(p.providerAbbr) as providers
    """
    params = {
        "user_name": user.user_name
    }
    results = graph.cypher_read_many(cypher, params)
    
    current_providers = results[0]['providers']
    new_providers = user.providers
    
    for provider in set(current_providers + new_providers):
        if provider in current_providers and provider not in new_providers:
            cypher = f"""
            MATCH (u:USER {{username: $user_name}})-[m:IS_MEMBER]->(p:ServiceProvider {{providerAbbr: $provider}})
            DELETE m
            """
            params = {
                "user_name": user.user_name,
                "provider": provider
            }
            graph.cypher_write(cypher, params)
        elif provider not in current_providers and provider in new_providers:
            cypher = f"""
            MATCH (u:USER {{username: $user_name}}), (p:ServiceProvider {{providerAbbr: $provider}})
            MERGE (u)-[:IS_MEMBER {{approved: 1}}]->(p)
            """
            params = {
                "user_name": user.user_name,
                "provider": provider
            }
            graph.cypher_write(cypher, params)
    
    if not user.is_admin == results[0]['u']['admin']:
        cypher = f"""
        MATCH (u:USER {{username: $user_name}})
        SET u.admin = $is_admin
        """
        params = {
            "user_name": user.user_name,
            "is_admin": user.is_admin
        }
        graph.cypher_write(cypher, params)
    
    return user

@router.delete('/users', response_model=schemas.UserDetail, include_in_schema=False)
async def remove_user(user_name: str, response: Response, jwt: dict=Depends(jwt_or_key_auth)):
    token = await get_admin_access_token()
    if await check_admin_role(jwt, token): 
        user = requests.get(f"https://scorpion.bi.denbi.de/admin/realms/scorpion/users?username={user_name}", headers={'Authorization': f'Bearer {token}'})
        user.raise_for_status()
        user = user.json()[0]
        user_id = user['id']
        
        response = requests.delete(f"https://scorpion.bi.denbi.de/admin/realms/scorpion/users/{user_id}", headers={'Authorization': f'Bearer {token}'})
        response.raise_for_status()
        
        graph=GraphConnection()
        cypher = f"""
        MATCH (u:USER {{id: $user_id}})
        DETACH DELETE u
        """
        params = {
            "user_id": user_id
        }
        graph.cypher_write(cypher, params)
        
    else:
        response.status_code=status.HTTP_403_FORBIDDEN
    return schemas.UserDetail(
        user_name=user['username'],
        email=user['email'],
        is_admin=False,
        providers=[]
    )

@router.get('/tokens', include_in_schema=False)
async def get_token(current_user: dict = Depends(jwt_or_key_auth)):
    graph = GraphConnection()
    cypher=f"""
    MATCH (u:USER {{id: $user_id}})-[:HAS_TOKEN]->(t:TOKEN)
    RETURN t {{.name}}
    """
    params = {
        "user_id": current_user['sub']
    }
    results = graph.cypher_read_many(cypher, params)
    tokens = []
    for result in results:
        tokens.append(result['t']['name'])
    return tokens

@router.post('/tokens', include_in_schema=False)
async def create_token(body: schemas.TokenCreate, current_user: dict = Depends(jwt_or_key_auth)):
    graph = GraphConnection()
    cypher=f"""
    MATCH (u:USER {{id: $user_id}})--(t:TOKEN {{name: $name}})
    RETURN t
    """
    params = {
        "user_id": current_user['sub'],
        "name": body.name
    }
    results = graph.cypher_read(cypher, params)
    if results:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Token name already exists"
        )
    
    neo_user = neo_models.User.match(current_user['sub'])
    token = neo_models.Token(value=uuid4().hex, name=body.name)
    token.create()
    hasToken = neo_models.HasToken(source=neo_user, target=token)
    hasToken.merge()

    return token.value

@router.delete('/tokens', include_in_schema=False)
async def delete_token(token: str, current_user: dict = Depends(jwt_or_key_auth)):
    graph = GraphConnection()
    cypher=f"""
    MATCH (u:USER {{id: $user_id}})-[h:HAS_TOKEN]->(t:TOKEN {{name: $token}})
    DELETE h, t
    """
    params = {
        "user_id": current_user['sub'],
        "token": token
    }
    try:
        graph.cypher_write(cypher, params)
        return True
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Token not found"
        )