from pydantic import BaseModel

class CreateRequestSchema(BaseModel):  
    name: str 
    age: int
    address: str 

class CreateResponseSchema(BaseModel):
    name: str 
    age: int 
    address: str