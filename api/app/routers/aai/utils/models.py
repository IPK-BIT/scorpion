from sqlalchemy import Column, String, Boolean
from uuid import uuid4

from utils.sqlite_database import Base

class User(Base):
    __tablename__="users"
    
    user_id = Column(String, primary_key=True, index=True, default=str(uuid4()))
    user_name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    salt = Column(String)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    accepted = Column(Boolean, default=False)
    
class Request(Base):
    __tablename__="requests"
    
    request_id = Column(String, primary_key=True, index=True, default=str(uuid4()))
    user_id = Column(String)
    providers = Column(String)