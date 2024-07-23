from pydantic import BaseModel

class UserBase(BaseModel):
    user_name: str
    email: str
    
class UserCreate(UserBase):
    password: str
    
class User(UserBase):
    user_id: str
    
class UserLogin(BaseModel):
    detail: str
    token: str|None
    
class UserDetail(UserBase):
    is_admin: bool
    providers: list[str]

class TokenCreate(BaseModel):
    name: str

class Request(BaseModel):
    id: str
    mail: str
    username: str
    provider: str