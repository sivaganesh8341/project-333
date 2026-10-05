from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.masterdata_schema import MasterdataCreate, MasterdataOut, UpdateMasterdata
from app.crud.masterdata_crud import create_masterdata, get_active_product, fetch_product_by_id, remove_masterdata, update_masterdata
from app.database.session import get_db

router = APIRouter(prefix="/masterdata", tags=["masterdata"])

@router.post("/", response_model=MasterdataOut, status_code=status.HTTP_201_CREATED)
def create_masterdata_route(masterdata: MasterdataCreate, db: Session = Depends(get_db)):
    return create_masterdata(masterdata, db)

@router.get("/products", response_model=List[MasterdataOut])
def get_active_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    return get_active_product(skip, limit, db)

@router.get("/product/{id}", response_model=MasterdataOut)
def get_product(id: int, db: Session = Depends(get_db)):
    return fetch_product_by_id(id, db)

@router.delete("/delete/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    return remove_masterdata(id, db)

@router.put("/product/{id}")
def update_product(id: int, request: UpdateMasterdata, db: Session = Depends(get_db)):
    return update_masterdata(id, request, db)
