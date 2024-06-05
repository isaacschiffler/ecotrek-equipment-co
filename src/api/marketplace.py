from fastapi import APIRouter, Depends
from pydantic import BaseModel
import sqlalchemy
from sqlalchemy.sql import func
from sqlalchemy import text
from src import database as db
import time

router = APIRouter(
    prefix="/marketplace",
    tags=["marketplace"],
)

class newProduct(BaseModel):
    productName: str
    user_id: int
    quantity: int
    price: int
    condition: str
    description: str

@router.post("/{listingID}")
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
    startTime = time.time()
    with db.engine.begin() as connection:
        # update quantity level of item; as of now, money handling is done between users, so our money ledger does not change
        connection.execute(sqlalchemy.text("""UPDATE marketplace 
                                                SET quantity = quantity - :quantity
                                                WHERE id = :listingID
                                                AND quantity >= :quantity
                                            """), 
                                            {'listingID': listingID, 'quantity': quantity})
        product_details = connection.execute(text("""SELECT product_name, price FROM marketplace WHERE id = :id """), {"id": listingID}).fetchone()
        
        if product_details is None:
            return {"Listing with id {} Does Not Exist.".format(listingID)}

    name = product_details.product_name
    price = product_details.price
    
    money_paid = price * quantity
    
    endTime = time.time()
    print("TIMING:", endTime - startTime) 
    return {"item_sold": name,
            "quantity": quantity,
            "money_paid": money_paid
            }


@router.post("/")
def marketplace_list(newListing: newProduct):
    """ 
    List Item

    Request:
    {
        "productName": "string",
        "user_id": "integer",
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
    startTime = time.time()
    with db.engine.begin() as connection:
        try:
            listingID = connection.execute(sqlalchemy.text("""INSERT INTO marketplace
                                                        (product_name, quantity, price, condition, description, user_id) VALUES
                                                        (:productName, :quantity, :price, :condition, :description, :user_id)
                                                        RETURNING id"""),
                                                        [{
                                                            'productName': newListing.productName,
                                                            'quantity': newListing.quantity,
                                                            'price': newListing.price,
                                                            'condition': newListing.condition,
                                                            'description': newListing.description,
                                                            'user_id': newListing.user_id
                                                        }]).fetchone()[0]
        except:
            return {"success": False, "message": "Invalid User ID"}

    endTime = time.time()
    print("TIMING:", endTime - startTime) 
    return  {"listingID": listingID}
    
                

