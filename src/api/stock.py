from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from sqlalchemy.sql import func
from sqlalchemy import text
from src import database as db


router = APIRouter(
    prefix="/stock",
    tags=["stock"],
    dependencies=[Depends(auth.get_api_key)],
)

class Stock(BaseModel):
    sku: str
    category:str
    price: int
    quantity: int

@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Stock]):
    """ 
    Planning wholesale purchase:
    Request:
    [
        {
            "sku": "string",
            "category": "string",
            "price": "integer",
            "quantity": "integer"
        }
    ]
    Response:
    [
        {
            "sku": "string", /* Must match a sku from the catalog just passed in this call */
            "quantity": "integer" /* A number between 1 and the quantity available for sale */
        }
    ]
    """
    with db.engine.begin() as connection:
        total_money = connection.execute(sqlalchemy.text("SELECT SUM(change) AS money FROM money_ledger")).fetchone()[0]
        print(total_money)
    money_count = 0
    quant = 0
    stock_plan = []
    for i in range(len(wholesale_catalog)):
        if (wholesale_catalog[i].price + money_count <= total_money):
            quant += 1
            stock_plan.append({
                "sku": wholesale_catalog[i].sku,
                "quantity": quant
            })
            money_count += wholesale_catalog[i].price

    return stock_plan
                

