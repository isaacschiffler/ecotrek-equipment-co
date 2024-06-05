from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
from enum import Enum
import sqlalchemy
from src import database as db
from datetime import datetime
from math import ceil
import time

router = APIRouter(
    prefix="/carts",
    tags=["cart"],
)

@router.post("/")
def create_cart(userID: int):
    """ 
    REQ: 
    { "userID": "integer" }
    RES:
    { "cartID": "integer" }
    """
    startTime = time.time()
    with db.engine.begin() as connection:
        user_exists = connection.execute(
            sqlalchemy.text("SELECT COUNT(id) FROM users WHERE id = :user_id"),
        {"user_id": userID}
        ).scalar() > 0
        
        if not user_exists:
            return {"Error": "User with ID {} does not exist.".format(userID)}
        
        # user exists in users
        cart_id = connection.execute(
            sqlalchemy.text("""INSERT INTO carts (user_id)
                            VALUES (:user_id) RETURNING id"""),
            {"user_id": userID}
            ).scalar_one()
    

    print("creating cart for user {} with id {}".format(userID, cart_id))

    endTime = time.time()
    print("TIMING:", endTime - startTime) 
    return {"cartID": cart_id}
    

class CartItem(BaseModel):
    quantity: int
    

@router.post("/{cart_id}/items/{productID}")
def set_item_quantity(cart_id: int, product_id: int, cart_item: CartItem):
    """ add quantity of items 
    REQ
    {
    "quantity": "integer"
    }
    RES
    {
    "success": "boolean",
    "message": "string"
    }

    """
    startTime = time.time()
    with db.engine.begin() as connection:
        # Check if product exists
        product_exists = connection.execute(
            sqlalchemy.text("SELECT 1 FROM products WHERE id = :product_id"),
            {'product_id': product_id}
        ).scalar()

        # Check if cart exists
        cart_exists = connection.execute(
            sqlalchemy.text("SELECT 1 FROM carts WHERE id = :cart_id"),
            {'cart_id': cart_id}
        ).scalar()

        if not product_exists or not cart_exists:
            return {"success": False, "message": "Invalid product or cart id passed. "}
        
        # Check if product already exists in cart
        existing_item = connection.execute(
            sqlalchemy.text("""
                SELECT 1 FROM cart_items
                WHERE cart_id = :cart_id AND product_id = :product_id
            """),
            {
                'cart_id': cart_id,
                'product_id': product_id
            }
        ).scalar()

        if existing_item:
            # Update quantity using UPDATE
            connection.execute(
                sqlalchemy.text("""
                    UPDATE cart_items
                    SET quantity = quantity + :quantity
                    WHERE cart_id = :cart_id AND product_id = :product_id
                """),
                {
                    'cart_id': cart_id,
                    'product_id': product_id,
                    'quantity': cart_item.quantity
                }
            )
            print("Updated quantity in cart " + str(cart_id) + ". Product id: " + str(product_id))
        else:
            # Creating new cart
            connection.execute(sqlalchemy.text("""INSERT INTO cart_items (cart_id, product_id, quantity, price)
                                           SELECT :cart_id, :product_id, :quantity, products.sale_price
                                           FROM products
                                           WHERE products.id = :product_id
                                           """),
                                           {
                                               'cart_id': cart_id,
                                               'quantity': cart_item.quantity,
                                               'product_id': product_id
                                           })
        
            print("new entry in cart " + str(cart_id) + ". Product id: " + str(product_id))

    endTime = time.time()
    print("TIMING:", endTime - startTime) 
    return {"success": True, "message": "OK"}


class CartCheckout(BaseModel):
    payment: str

@router.post("/{cart_id}/checkout")
def checkout(cart_id: int, cart_checkout: CartCheckout):
    """Subtract item quantity and add money
    REQ
    {
    "payment": "string"
    }
    RES
    {
    "num_items_bought": "integer",
    "money_paid": "integer"
    }
    """
    startTime = time.time()
    with db.engine.begin() as connection:
        # Check if cart exists
        cart_exists = connection.execute(
            sqlalchemy.text("SELECT 1 FROM carts WHERE id = :cart_id"),
            {'cart_id': cart_id}
        ).scalar()

        if not cart_exists:
            return {"success": False, "message": "Invalid cart id passed. "}

        # insert into processed
        trans_id = connection.execute(sqlalchemy.text("""
            INSERT INTO processed(job_id, type) 
            VALUES
            (:job_id, 'item_sale') RETURNING id;
            """),
            {
                'job_id': cart_id
            }).fetchone()[0]

        connection.execute(sqlalchemy.text("""                    
            INSERT INTO stock_ledger (trans_id, product_id, change, description)
            SELECT :trans_id, product_id, -1 * quantity, :description
            FROM cart_items
            WHERE cart_items.cart_id = :cart_id"""),
            {
                'trans_id': trans_id,
                'description': 'sale',
                'cart_id': cart_id
            })
        
        connection.execute(sqlalchemy.text("""
            INSERT INTO money_ledger(trans_id, change, description)
            SELECT :trans_id, SUM(quantity * price), :description
            FROM cart_items
            WHERE cart_items.cart_id = :cart_id
            GROUP BY cart_items.cart_id;"""),
            {
                'trans_id': trans_id,
                'cart_id': cart_id,
                'description': 'sale'
            })

        # get quantity of items sold
        quant_bought = connection.execute(sqlalchemy.text("SELECT SUM(change) as total FROM stock_ledger WHERE trans_id = :trans_id"),
                                          {
                                              'trans_id': trans_id
                                          }).fetchone().total * -1

        # get money paid
        income = connection.execute(sqlalchemy.text("SELECT change FROM money_ledger WHERE trans_id = :trans_id"),
                                    {
                                        'trans_id': trans_id
                                    }).fetchone().change
        
    print("stock bought: " + str(quant_bought) + " money paid: " + str(income))

    endTime = time.time()
    print("TIMING:", endTime - startTime) 
    return {"num_items_bought": quant_bought, "money_paid": income}