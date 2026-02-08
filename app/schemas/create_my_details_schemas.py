from pydantic import BaseModel

class CreateMyRequestSchema(BaseModel):
    name: str 
    age: int
    add: str 

class CreateMyResponseSchema(BaseModel):
    name: str 
    age: int 
    add: str 
