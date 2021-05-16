from sqlalchemy.orm import Session

from . import models


def get_suppliers(db: Session):
    return db.query(models.Supplier).all()


def get_supplier(db: Session, id: int):
    return (
        db.query(models.Supplier).filter(models.Supplierr.SupplierID == id).first()
    )
