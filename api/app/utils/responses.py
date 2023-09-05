from pydantic import BaseModel
from typing import TypeVar, Generic
from utils import schemas

T = TypeVar('T')

class Response(BaseModel, Generic[T]):
    metadata: schemas.Metadata
    result: list[T]