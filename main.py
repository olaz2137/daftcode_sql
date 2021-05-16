import sqlite3

from fastapi import Cookie, FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from typing import List


app = FastAPI()

@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()

#4.1
@app.get("/categories")
async def categories():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute("SELECT CategoryID, CategoryName FROM Categories").fetchall()
    return {"categories" : [{"id": x['CategoryID'], "name": x['CategoryName']} for x in data]}

@app.get("/customers")
async def customers():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute("SELECT CustomerID, CompanyName, Address || ' ' || PostalCode || ' '|| City ||' '|| Country AS ConcatenatedString FROM Customers").fetchall()
    return {"customers" : [{"id": x['CustomerID'], "name": x['CompanyName'], "full_address": x['ConcatenatedString']} for x in data]}

#4.2
@app.get("/products/{id}")
async def products(id:int):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute("SELECT ProductID as id, ProductName as name FROM Products WHERE ProductID = :id",{'id': id}).fetchone()
    if data is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return data

#4.3
@app.get("/employees")
async def employees(*, limit:int = -1, offset:int = 0, order:str = ""):
    if order not in {"first_name","last_name","city",""}:
        raise HTTPException(status_code=400, detail="Bad Request")
    if order == "":
        order = 'id'
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(f"SELECT EmployeeID AS id,LastName AS last_name , FirstName AS first_name , City as city FROM Employees ORDER BY {order} LIMIT :limit OFFSET :offset",{'limit':limit,'offset':offset}).fetchall()
    return {"employees":data}

#4.4
@app.get("/products_extended")
async def products_extended():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute("SELECT Products.ProductID as id, Products.ProductName as name, Categories.CategoryName as category, Suppliers.CompanyName as supplier FROM Products JOIN Categories ON Products.CategoryID = Categories.CategoryID , Suppliers ON Products.SupplierID = Suppliers.SupplierID ORDER BY id").fetchall()

    return {"products_extended":data}

#4.5
@app.get("/products/{id}/orders")
async def orders(id:int):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute("SELECT Orders.OrderId AS id, Customers.CompanyName AS customer, [Order Details].Quantity AS quantity, round((([Order Details].UnitPrice*quantity)-([Order Details].Discount*[Order Details].UnitPrice*quantity)),2) AS total_price FROM Orders JOIN ([Order Details] JOIN Products ON [Order Details].ProductID = Products.ProductID) ON [Order Details].OrderID = Orders.OrderID, Customers ON Customers.CustomerID = Orders.CustomerID  WHERE Products.ProductID = :id",{'id': id}).fetchall()
    if data == []:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"orders":data}

#4.6
class Category(BaseModel):
    name:str

@app.post("/categories",status_code = 201)
async def post_categories(category: Category):
    cursor = app.db_connection.execute(
        f"INSERT INTO Categories (CategoryName) VALUES ('{category.name}')"
    )
    app.db_connection.commit()
    return {
        "id": cursor.lastrowid,
        "name": category.name
    }

@app.put("/categories/{id}")
async def put_categories(*,id:int,category: Category):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(
        "SELECT* FROM Categories WHERE CategoryID =?",(id,)).fetchone()
    if data is None:
        raise HTTPException(status_code=404, detail="Item not found")
    cursor = app.db_connection.execute(
        "UPDATE Categories SET CategoryName = ? WHERE CategoryID = ?",(category.name, id,)
    )
    app.db_connection.commit()
    return {
        "id": id,
        "name": category.name
    }

@app.delete("/categories/{id}")
async def delete_categories(id:int):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(
        "SELECT* FROM Categories WHERE CategoryID = :id",{"id":id}).fetchone()
    if data is None:
        raise HTTPException(status_code=404, detail="Item not found")
    cursor = app.db_connection.execute(
        "DELETE FROM Categories WHERE CategoryID = :id", {"id":id}
    )
    app.db_connection.commit()
    return {"deleted": cursor.rowcount}
#5

from fastapi import FastAPI

from .views import router as northwind_api_router

#app = FastAPI()

app.include_router(northwind_api_router, tags=["northwind"])
