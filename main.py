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
    categories = app.db_connection.execute("SELECT CategoryID, CategoryName FROM Categories").fetchall()
    return {"categories" : [{"id": x['CategoryID'], "name": x['CategoryName']} for x in categories]}

@app.get("/customers")
async def customers():
    app.db_connection.row_factory = sqlite3.Row
    customers = app.db_connection.execute("SELECT CustomerID, CompanyName, (COALESCE(Address, '') || ' ' || COALESCE(PostalCode, '') || ' ' || COALESCE(City, '') || ' ' || COALESCE(Country, '')) AS ConcatenatedString FROM Customers ORDER BY CustomerID").fetchall()
    return {"customers" : [{"id": x['CustomerID'], "name": x['CompanyName'], "full_address":  x['ConcatenatedString']} for x in customers]}

