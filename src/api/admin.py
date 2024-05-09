from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/reset")
def reset():
    """
    TEST....
    """
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("DELETE FROM cart_items"))
        connection.execute(sqlalchemy.text("DELETE FROM carts"))
        connection.execute(sqlalchemy.text("DELETE FROM customers"))
        connection.execute(sqlalchemy.text("DELETE FROM processed"))
        connection.execute(sqlalchemy.text("DELETE FROM stock_ledger"))
        connection.execute(sqlalchemy.text("DELETE FROM money_ledger"))
        connection.execute(sqlalchemy.text("""INSERT INTO money_ledger (change, description)
                                              VALUES (1000, 'seed money')
                                           """))


                 
    return "OK"

