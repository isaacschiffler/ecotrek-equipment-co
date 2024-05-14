import sqlalchemy
from src import database as db
from fastapi import APIRouter

router = APIRouter()


@router.get("/catalog/", tags=["catalog"])
def get_catalog():
    catalog = []
    with db.engine.begin() as connection:
        stock = connection.execute(sqlalchemy.text("""SELECT products.id, products.name, products.description, SUM(change) AS quantity, products.sale_price, products.daily_rental_price, categories.type
                                                      FROM stock_ledger
                                                      JOIN products ON products.id = stock_ledger.product_id
                                                      JOIN categories ON products.category_id = categories.id
                                                      GROUP BY products.id, products.name, products.description, products.sale_price, products.daily_rental_price, categories.type;
                                                   """)).fetchall()
        
        print("Current inventory:", stock)

        for item in stock:
            catalog.append(
                {
                    "productID": item.id,
                    "product_name": item.name,
                    "category": item.type,
                    "sale price": item.sale_price,
                    "rental price": item.daily_rental_price,
                    "stock": item.quantity,
                    "description": item.description
                }
            )
                
    return catalog
