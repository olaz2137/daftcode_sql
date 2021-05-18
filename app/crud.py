from sqlalchemy.orm import Session

from . import models


def get_suppliers(db: Session):
    return db.query(models.Supplier).all()


def get_supplier(db: Session, supplier_id: int):
    return (
        db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id).first()
    )

def get_supplier_products(db: Session, supplier_id:int):
    return db.query(models.Product).filter(models.Product.SupplierID == supplier_id).order_by(models.Product.product_id.desc()).all()
    
