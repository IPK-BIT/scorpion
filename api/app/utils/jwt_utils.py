from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import secrets
import bcrypt
import jwt
from datetime import datetime, timedelta
from utils.dependencies import get_db
from routers.aai.utils import models, schemas

from icecream import ic   

_PRIVATE_KEY_ = b''
for line in open("resources/jwt-key.pem", "rb"):
    _PRIVATE_KEY_ += line
    
_PUBLIC_KEY_ = b''
for line in open("resources/jwt-key.crt", "rb"):
    _PUBLIC_KEY_ += line
    
def build(user: schemas.User):
    payload = {
        "exp": datetime.now()+timedelta(hours=1),
        "id": user.user_id
    }
    return jwt.encode(payload, _PRIVATE_KEY_, algorithm="RS256")

def read(token: str):
    return jwt.decode(token, _PUBLIC_KEY_, algorithms=["RS256"])


def authenticate(db: Session, username: str, password: str):
    db_user = db.query(models.User).filter(models.User.email == username).first()
    if db_user is None:
        db_user = models.User(email="no user", hashed_password="no password", salt="no salt")
    
    if not db_user.accepted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Request not accepted by an administrator"
        )
    
    username_bytes = username.encode("utf8")
    password_bytes = bcrypt.hashpw(password.encode("utf8"),db_user.salt)
    db_username_bytes = db_user.email.encode("utf8")
    
    is_correct_username = secrets.compare_digest(username_bytes, db_username_bytes)
    is_correct_password = secrets.compare_digest(password_bytes, db_user.hashed_password)
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"}
        )
    return db_user

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code.")
        
    def verify_jwt(self, jwt_token: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = read(jwt_token)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid