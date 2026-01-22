from fastapi import APIRouter, Depends, HTTPException
from schemas.create_my_details_schemas import CreateMyResponseSchema
from core.cointer import get_create_my_details_service
from service.create_my_details_service import CreateMyDetailsService
from exceptions.create_my_details_exception import NameNotFound, AddressNotFound, AgeNotFound

router = APIRouter(prefix= "/create_my_details", tags=["Create My Details"])

@router.post("", response_model=CreateMyResponseSchema)
async def create_my_details(
    payload: CreateMyResponseSchema,
    service: CreateMyDetailsService = Depends(get_create_my_details_service)
):
    try:
        create_details = await service.create_my_details(payload)
        return create_details
    except NameNotFound as e:
        raise HTTPException(
            status_code= 400,
            detail= "Name not Found Try to add your name first"
        )
    except AgeNotFound:
        raise HTTPException(
            status_code=400,
            detail="Age is not found try to add your age first"
        )
    
    except AddressNotFound:
        raise HTTPException(
            status_code=400,
            detail="Address not found try to add your Address first"
        )
         
    