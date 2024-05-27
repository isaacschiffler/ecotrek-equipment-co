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

        # Adding products to the products table
        connection.execute(sqlalchemy.text("""
            INSERT INTO products (sku, name, description, category_id, sale_price, daily_rental_price)
            VALUES 
                ('RED_JANSPORT_BCKPK', 'Red Jansport Backpack', 'Primarily for everyday use', 
                (SELECT id FROM categories WHERE type='BACKPACKING'), 70, 5),
                ('BLU_CAMP_TENT', 'Blue Camping Tent', 'Spacious tent for camping', 
                (SELECT id FROM categories WHERE type='CAMPING'), 150, 15),
                ('GRN_CAMP_STOVE', 'Green Camping Stove', 'Portable stove for outdoor cooking', 
                (SELECT id FROM categories WHERE type='CAMPING'), 80, 8),
                ('CAMP_UTENSILS_SET', 'Camping Utensils Set', 'Set of essential utensils for camping', 
                (SELECT id FROM categories WHERE type='CAMPING'), 30, 3),
                ('LED_FLASHLIGHT', 'LED Flashlight', 'High-lumen LED flashlight for camping', 
                (SELECT id FROM categories WHERE type='CAMPING'), 25, 2),
                ('CAMP_SLEEPING_BAG', 'Camping Sleeping Bag', 'Warm and comfortable sleeping bag', 
                (SELECT id FROM categories WHERE type='CAMPING'), 60, 6),
                ('PORTABLE_STOVE', 'Portable Stove', 'Compact and efficient portable stove', 
                (SELECT id FROM categories WHERE type='CAMPING'), 90, 9),
                ('CAMPING_CHAIR', 'Camping Chair', 'Comfortable and foldable camping chair', 
                (SELECT id FROM categories WHERE type='CAMPING'), 40, 4)
        """))

        # Adding multiple job entries to the processed table in one query
        connection.execute(sqlalchemy.text("""INSERT INTO processed (job_id, type)
                                            VALUES (1, 'stock_delivery'),
                                                    (2, 'stock_delivery'),
                                                    (3, 'stock_delivery'),
                                                    (4, 'stock_delivery'),
                                                    (5, 'stock_delivery'),
                                                    (6, 'stock_delivery'),
                                                    (7, 'stock_delivery'),
                                                    (8, 'stock_delivery'),
                                                    (9, 'stock_delivery')"""))

        # Inserting stock into the stock_ledger for each product in the products table
        connection.execute(sqlalchemy.text("""
            INSERT INTO stock_ledger (product_id, change, description, trans_id)
            VALUES 
                ((SELECT id FROM products WHERE sku='RED_JANSPORT_BCKPK'), 5, 
                'Delivered 5 units of RED_JANSPORT_BCKPK', 
                (SELECT id FROM processed WHERE job_id=1 AND type='stock_delivery')),
                ((SELECT id FROM products WHERE sku='BLU_CAMP_TENT'), 10, 
                'Delivered 10 units of BLU_CAMP_TENT', 
                (SELECT id FROM processed WHERE job_id=1 AND type='stock_delivery')),
                ((SELECT id FROM products WHERE sku='GRN_CAMP_STOVE'), 7, 
                'Delivered 7 units of GRN_CAMP_STOVE', 
                (SELECT id FROM processed WHERE job_id=1 AND type='stock_delivery')),
                ((SELECT id FROM products WHERE sku='CAMP_UTENSILS_SET'), 15, 
                'Delivered 15 units of CAMP_UTENSILS_SET', 
                (SELECT id FROM processed WHERE job_id=1 AND type='stock_delivery')),
                ((SELECT id FROM products WHERE sku='LED_FLASHLIGHT'), 20, 
                'Delivered 20 units of LED_FLASHLIGHT', 
                (SELECT id FROM processed WHERE job_id=1 AND type='stock_delivery')),
                ((SELECT id FROM products WHERE sku='CAMP_SLEEPING_BAG'), 12, 
                'Delivered 12 units of CAMP_SLEEPING_BAG', 
                (SELECT id FROM processed WHERE job_id=1 AND type='stock_delivery')),
                ((SELECT id FROM products WHERE sku='PORTABLE_STOVE'), 8, 
                'Delivered 8 units of PORTABLE_STOVE', 
                (SELECT id FROM processed WHERE job_id=1 AND type='stock_delivery')),
                ((SELECT id FROM products WHERE sku='CAMPING_CHAIR'), 10, 
                'Delivered 10 units of CAMPING_CHAIR', 
                (SELECT id FROM processed WHERE job_id=1 AND type='stock_delivery'))
        """))
   
    return "OK"

