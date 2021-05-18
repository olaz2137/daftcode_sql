from pydantic import BaseModel, PositiveInt, constr, AnyUrl
from typing import Optional

class Supplier(BaseModel):

    SupplierID: PositiveInt
    CompanyName: Optional[constr(max_length=40)]
    ContactName: Optional[constr(max_length=30)]
    ContactTitle: Optional[constr(max_length=30)]
    Address: Optional[constr(max_length=60)]
    City: Optional[constr(max_length=15)]
    Region: Optional[constr(max_length=15)]
    PostalCode: Optional[constr(max_length=10)]
    Country: Optional[constr(max_length=15)]
    Phone: Optional[constr(max_length=24)]
    Fax: Optional[constr(max_length=24)]
    HomePage: Optional[str]

    
    class Config:
        orm_mode = True
        
class Suppliers(BaseModel):

    SupplierID: PositiveInt
    CompanyName: Optional[constr(max_length=40)]

    
    class Config:
        orm_mode = True
        
class Category(BaseModel):
    CategoryID: PositiveInt
    CategoryName: Optional[constr(max_length=40)]

    class Config:
        orm_mode = True
        
class SupplierProducts(BaseModel):
    
    ProductID : PositiveInt
    ProductName : Optional[constr(max_length=40)]
    Category : Optional[Category]
    Discontinued : PositiveInt
    
    class Config:
        orm_mode = True
