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
)

class Stock(BaseModel):
    sku: str
    category_id:int
    price: int
    quantity: int

@router.post("/deliver/{order_id}")
def post_deliver_stock(stock_plan: list[Stock], order_id: int):
    total_cost = 0
    with db.engine.begin() as connection:
        try:
            # Generate a new transaction ID
            trans_id_result = connection.execute(sqlalchemy.text("""
                INSERT INTO processed (job_id, type) VALUES (:job_id, :type) RETURNING id;
            """), {'job_id': order_id, 'type': 'stock_delivery'})
            trans_id = trans_id_result.fetchone()[0]

            for item in stock_plan:
                total_cost += item.price * item.quantity

                # Check if the item exists in the products table
                product_result = connection.execute(sqlalchemy.text("""
                    SELECT id FROM products WHERE sku = :sku;
                """), {'sku': item.sku})
                existing_product = product_result.fetchone()

                if existing_product:
                    # Update the existing product
                    product_id = existing_product[0]
                    connection.execute(sqlalchemy.text("""
                        UPDATE products 
                        SET sale_price = :price, category_id = :category_id 
                        WHERE id = :product_id;
                    """), {
                        'price': item.price,
                        'category_id': item.category_id,
                        'product_id': product_id
                    })
                else:
                    # Insert a new product
                    product_result = connection.execute(sqlalchemy.text("""
                        INSERT INTO products (sku, sale_price, category_id)
                        VALUES (:sku, :price, :category_id)
                        RETURNING id;
                    """), {
                        'sku': item.sku,
                        'price': item.price,
                        'category_id': item.category_id
                    })
                    product_id = product_result.fetchone()[0]
                # Insert into stock_ledger table
                connection.execute(sqlalchemy.text("""
                    INSERT INTO stock_ledger (product_id, change, description, trans_id)
                    VALUES (:product_id, :change, :description, :trans_id);
                """), {
                    'product_id': product_id,
                    'change': item.quantity,
                    'description': f"Delivered {item.quantity} units of {item.sku}",
                    'trans_id': trans_id
                })

            # Insert into money_ledger table
            connection.execute(sqlalchemy.text("""
                INSERT INTO money_ledger (change, description)
                VALUES (:cost, 'deliver_stock_plan');
            """), {'cost': -total_cost})

            print(f"Delivered these products: {stock_plan}")

            return "OK"
        except Exception as e:
            print(f"An error occurred: {e}")
            

@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Stock]):
    """ 
    Planning wholesale purchase:
    Request:
    [
        {
            "sku": "string",
            "category_id": "integer",
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
        if total_money is None:
            total_money = 0
        print(total_money)

    money_count = 0
    stock_plan = []
    
    # Sort catalog by price ascending
    wholesale_catalog.sort(key=lambda x: x.price)
    
    for item in wholesale_catalog:
        # Calculate the maximum quantity that can be purchased
        max_quantity = min(item.quantity, (total_money - money_count) // item.price)
        if max_quantity > 0:
            stock_plan.append({
                "sku": item.sku,
                "quantity": max_quantity,
                "price": item.price,
                "category_id": item.category_id
            })
            money_count += max_quantity * item.price

    print(f"Stock plan: {stock_plan}")

    return stock_plan
                

