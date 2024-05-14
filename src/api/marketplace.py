from fastapi import APIRouter, Depends
from pydantic import BaseModel
import sqlalchemy
from sqlalchemy.sql import func
from sqlalchemy import text
from src import database as db


router = APIRouter(
    prefix="/marketplace",
    tags=["marketplace"],
)

class newProduct(BaseModel):
    productName: str
    quantity:int
    price: int
    condition: str
    description: str

@router.post("/marketplace/{listingID}")
def marketplace_sell(listingID: int, quantity: int):
    """
    Sell Item

    Request:
    {
        "quantity": "integer"
    }

    Response:
    {
        "item_sold": "string",
        "quantity": "integer",
        "money_paid": "integer"
    }
    """

    with db.engine.begin() as connection:
        # update quantity level of item; as of now, money handling is done between users, so our money ledger does not change
        connection.execute(sqlalchemy.text("""UPDATE marketplace 
                                           SET quantity = (SELECT quantity FROM marketplace where id = :listingID) - :quantity
                                           WHERE id = :listingID"""), 
                                           [{
                                               'listingID': listingID,
                                               'quantity': quantity
                                           }])

    return "OK"


@router.post("/marketplace")
def marketplace_list(newListing: newProduct):
    """ 
    List Item

    Request:
    {
        "productName": "string",
        "quantity": "integer",
        "price": "integer",
        "condition": "string",
        "description": "string"
    }

    Response:
    {
        "listingID": "integer"
    }
    """
    with db.engine.begin() as connection:
        listingID = connection.execute(sqlalchemy.text("""INSERT INTO marketplace
                                                    (product_name, quantity, price, condition, description) VALUES
                                                    (:productName, :quantity, :price, :condition, :description)
                                                    returning id"""),
                                                    [{
                                                        'productName': newListing.productName,
                                                        'quantity': newListing.quantity,
                                                        'price': newListing.price,
                                                        'condition': newListing.condition,
                                                        'description': newListing.description
                                                    }]).fetchone()[0]

    return listingID
                

