from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from icecream import ic

from utils.dependencies import get_db
from utils import jwt_utils
from routers.aai.utils import crud, schemas, models

router = APIRouter(
    prefix="/aai",
    tags=["AAI"]
)

security = HTTPBasic()

@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    db_user = crud.get_user_by_name(db, name=user.user_name)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already registered"
        )
    return crud.create_user(db, user)

@router.post("/login", response_model=schemas.UserLogin)
def login_user(
    credentials: HTTPBasicCredentials = Depends(security), 
    db: Session = Depends(get_db)
):
    user = None
    if not crud.is_valid_email(credentials.username):
        try:
            user = crud.get_user_by_name(db, name=credentials.username)
        finally: 
            credentials.username = user.email
            
    authenticated_user = jwt_utils.authenticate(
        db, 
        credentials.username, 
        credentials.password
    )
    token = jwt_utils.build(authenticated_user)
    return schemas.UserLogin(
        detail="Login successful",
        token=token
    )

@router.post("/logout", response_model=schemas.UserLogin)
def logout_user():
    return schemas.UserLogin(
        detail="Logout successful",
        token=None
    )

@router.get('/details', response_model=schemas.UserDetail)
def get_user(token: HTTPAuthorizationCredentials = Depends(jwt_utils.JWTBearer()), db: Session = Depends(get_db)):
    payload = jwt_utils.read(token)
    user: models.User = crud.get_user_by_id(db, payload["id"])
    providers: str = crud.get_user_memberships_by_id(payload["id"])
    return schemas.UserDetail(
        user_name=user.user_name,
        email=user.email,
        is_admin=user.is_admin,
        providers=providers
    )
    
@router.post('/requests/membership', response_model=schemas.Request, status_code=status.HTTP_201_CREATED)
def request_membership(providers: str, token: HTTPAuthorizationCredentials = Depends(jwt_utils.JWTBearer()), db: Session = Depends(get_db)):
    payload = jwt_utils.read(token)
    user: models.User = crud.get_user_by_id(db, payload["id"])
    return crud.create_request(db, user, providers)

@router.get('/requests/membership', response_model=list[schemas.Request], include_in_schema=False)
def get_membership_requests(token: HTTPAuthorizationCredentials = Depends(jwt_utils.JWTBearer()), db:Session = Depends(get_db)):
    requests: list[models.Request] = crud.get_requests(db, jwt_utils.read(token)["id"])
    response = []
    for request in requests:
        user: models.User = crud.get_user_by_id(db, request.user_id)
        response.append(schemas.Request(
            id= request.request_id,
            mail=user.email,
            username=user.user_name,
            provider=request.providers
        ))
    return response

@router.delete('/requests/membership', response_model=schemas.Request|None, include_in_schema=False)
def remove_membership_request(request_id:str, accept: bool, response: Response, token: HTTPAuthorizationCredentials = Depends(jwt_utils.JWTBearer()), db:Session=Depends(get_db)):
    if (not crud.get_user_by_id(db, jwt_utils.read(token)["id"]).is_admin):
        response.status_code=status.HTTP_403_FORBIDDEN
        return 
    return crud.remove_request(db, request_id, accept)

@router.get('/requests/registration', include_in_schema=False, response_model=list[schemas.User])
def get_open_registrations(token: HTTPAuthorizationCredentials = Depends(jwt_utils.JWTBearer()), db: Session = Depends(get_db)):
    db_users:list[models.User]=crud.get_open_requests(db)
    response:list[schemas.User]=[]
    for db_user in db_users:
        response.append(schemas.User(
            user_id=db_user.user_id,
            email=db_user.email,
            user_name=db_user.user_name
        ))
    return response

@router.delete('/requests/registration', include_in_schema=False, response_model=schemas.User)
def remove_registration_request(request_id:str, is_admin: bool, accept: bool, response: Response, token: HTTPAuthorizationCredentials = Depends(jwt_utils.JWTBearer()), db:Session = Depends(get_db)):
    if (not crud.get_user_by_id(db, jwt_utils.read(token)["id"]).is_admin):
        response.status_code=status.HTTP_403_FORBIDDEN
        return
    return crud.finish_registration(db, request_id, is_admin, accept)

@router.get('/users', response_model=list[schemas.UserDetail], include_in_schema=False)
def list_all_users(response: Response, token: HTTPAuthorizationCredentials = Depends(jwt_utils.JWTBearer()), db: Session = Depends(get_db)):
    if (not crud.get_user_by_id(db, jwt_utils.read(token)["id"]).is_admin):
        response.status_code=status.HTTP_403_FORBIDDEN
        return 
    db_users: list[models.User]=crud.get_users(db)
    results: list[schemas.UserDetail] = []
    for db_user in db_users:
        providers=crud.get_user_memberships_by_id(db_user.user_id)
        results.append(schemas.UserDetail(
            user_id=db_user.user_id,
            email=db_user.email,
            user_name=db_user.user_name,
            is_admin=db_user.is_admin,
            providers=providers
        ))
    return results

@router.put('/users', response_model=schemas.UserDetail, include_in_schema=False)
def update_user(user: schemas.UserDetail, response: Response, token: HTTPAuthorizationCredentials=Depends(jwt_utils.JWTBearer()), db:Session=Depends(get_db)):
    if (not crud.get_user_by_id(db, jwt_utils.read(token)["id"]).is_admin):
        response.status_code=status.HTTP_403_FORBIDDEN
        return
    return crud.update_user(db, user)

@router.delete('/users', response_model=schemas.UserDetail, include_in_schema=False)
def remove_user(user_name: str, response: Response, token: HTTPAuthorizationCredentials=Depends(jwt_utils.JWTBearer()), db: Session=Depends(get_db)):
    if (not crud.get_user_by_id(db, jwt_utils.read(token)["id"]).is_admin):
        response.status_code=status.HTTP_403_FORBIDDEN
        return
    return crud.remove_user(db, user_name)