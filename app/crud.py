from sqlalchemy.orm import Session

from . import models


def get_suppliers(db: Session):
    return db.query(models.Supplier).all()


def get_supplier(db: Session, supplier_id: int):
    return (
        db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id).first()
    )

def get_supplier_products(db: Session, supplier_id:int):
    return db.query(models.Product).join(models.Category).filter(models.Product.SupplierID == supplier_id).order_by(models.Product.ProductID.desc()).all()

def post_suppliers(db: Session, new_record: NewRecord):
    new_record_id = db.query(models.Supplier).count()+1
    new_record_result = models.Supplier(SupplierID = new_record_id, CompanyName = new_srecord.CompanyName, ContactName = new_record.ContactName,
                                          ContactTitle = new_record.ContactTitle,
                                          Address = new_record.Address,
                                          City = new_record.City,
                                          PostalCode = new_record.PostalCode,
                                          Country = new_record.Country,
                                          Phone = new_record.Phone)
    
    
    db.add(new_record_result)
    db.commit()
    return new_record_result
