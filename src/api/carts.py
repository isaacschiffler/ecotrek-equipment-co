from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
from enum import Enum
import sqlalchemy
from src import database as db
from datetime import datetime
from math import ceil


router = APIRouter(
    prefix="/carts",
    tags=["cart"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/")
def create_cart(userID: int):
    """ 
    REQ: 
    { "userID": "integer" }
    RES:
    { "cartID": "integer" }
    """
    with db.engine.begin() as connection:
        user_exists = connection.execute(
            sqlalchemy.text("SELECT COUNT(*) FROM users WHERE id = :user_id"),
            {"user_id": userID}
        ).scalar() > 0
        
        if not user_exists:
            return {"Error": f"User with ID {userID} does not exist."}
        
        # user exists in users
        cart_id = connection.execute(
            sqlalchemy.text("INSERT INTO carts (user_id) "
                            "VALUES (:user_id) RETURNING id"),
            {"user_id": userID}
        ).scalar_one()
    

        print(f"creating cart for user {userID} with id {cart_id}")

        return {"cartID": cart_id}