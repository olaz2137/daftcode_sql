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
    data = app.db_connection.execute("SELECT CustomerID, CompanyName, Address || ' ' || PostalCode || ' '|| City ||' '|| Country AS ConcatenatedString FROM Customers ORDER BY CustomerID").fetchall()
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
async def employees(*, limit:int, offset:int, order:str):
    if order not in {"first_name","last_name","city"}:
        raise HTTPException(status_code=400, detail="Bad Request")
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute("SELECT EmployeeID AS id,LastName AS last_name , FirstName AS first_name , City as city FROM Employees ORDER BY :order LIMIT :limit OFFSET :offset",{'order':order,'limit':limit,'offset':offset}).fetchall()
    return {"employees":data}
