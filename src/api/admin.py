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
        # Delete existing table entries IN ORDER of foreign key relations
        connection.execute(sqlalchemy.text("DELETE FROM cart_items"))
        connection.execute(sqlalchemy.text("DELETE FROM carts"))
        connection.execute(sqlalchemy.text("DELETE FROM users"))
        connection.execute(sqlalchemy.text("DELETE FROM stock_ledger"))
        connection.execute(sqlalchemy.text("DELETE FROM money_ledger"))
        connection.execute(sqlalchemy.text("DELETE FROM processed"))
        connection.execute(sqlalchemy.text("DELETE FROM products"))
        connection.execute(sqlalchemy.text("DELETE FROM categories"))
        connection.execute(sqlalchemy.text("DELETE FROM marketplace"))

        # Reset id incrementations to 1
        connection.execute(sqlalchemy.text("ALTER SEQUENCE carts_id_seq RESTART WITH 1;"))
        connection.execute(sqlalchemy.text("ALTER SEQUENCE stock_ledger_id_seq RESTART WITH 1;"))
        connection.execute(sqlalchemy.text("ALTER SEQUENCE money_ledger_id_seq RESTART WITH 1;"))
        connection.execute(sqlalchemy.text("ALTER SEQUENCE processed_id_seq RESTART WITH 1;"))
        connection.execute(sqlalchemy.text("ALTER SEQUENCE products_id_seq RESTART WITH 1;"))
        connection.execute(sqlalchemy.text("ALTER SEQUENCE categories_id_seq RESTART WITH 1;"))
        connection.execute(sqlalchemy.text("ALTER SEQUENCE marketplace_id_seq RESTART WITH 1;"))



        # Insert initial seed data
        connection.execute(sqlalchemy.text("""INSERT INTO money_ledger (change, description) 
                                              VALUES (1000, 'start with $1000 to spend')"""))

        connection.execute(sqlalchemy.text("""INSERT INTO categories(type, description) 
                                              VALUES ('SHELTER', Null), 
                                                     ('SLEEPING', Null), 
                                                     ('BACKPACKING', Null), 
                                                     ('COOKING', Null)"""))

        connection.execute(sqlalchemy.text("""INSERT INTO products (sku, name, description, category_id, sale_price, daily_rental_price)
                                              VALUES ('RED_JANSPORT_BCKPK', 'Red Jansport Backpack', 'Primarily for everyday use', 
                                                      (SELECT id FROM categories WHERE type='BACKPACKING'), 70, 5)"""))

        connection.execute(sqlalchemy.text("""INSERT INTO processed (job_id, type)
                                              VALUES (1, 'stock_delivery')"""))

        connection.execute(sqlalchemy.text("""INSERT INTO stock_ledger (product_id, change, description, trans_id)
                                              VALUES ((SELECT id FROM products WHERE sku='RED_JANSPORT_BCKPK'), 5, 
                                                      'Delivered 5 units of RED_JANSPORT_BCKPK', 
                                                      (SELECT id FROM processed WHERE job_id=1 AND type='stock_delivery'))"""))
                 
    return "OK"

