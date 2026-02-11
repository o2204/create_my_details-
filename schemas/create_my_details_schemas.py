from pydantic import BaseModel

class CreateMyRequestSchema(BaseModel):
    name: str 
    age: int
    address: str 

class CreateMyResponseSchema(BaseModel):
    name: str 
    age: int 
    address: str 
