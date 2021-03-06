from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db

router = APIRouter()


@router.get("/suppliers/{supplier_id}", response_model=schemas.Supplier)
async def get_supplier(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier


@router.get("/suppliers", response_model=List[schemas.Suppliers])
async def get_suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)

@router.get("/suppliers/{supplier_id}/products",response_model=List[schemas.SupplierProducts])
async def get_supplier_products(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier_products = crud.get_supplier_products(db, supplier_id)
    if db_supplier_products == []:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier_products

@router.post("/suppliers", response_model=schemas.Supplier, status_code=201)
async def post_suppliers(new_record: schemas.NewRecord, db: Session = Depends(get_db)):
    db_new_record = crud.post_suppliers(db, new_record)
    return crud.get_suppliers(db)
