import sqlalchemy
from src import database as db
from fastapi import APIRouter
from sqlalchemy.sql import select, func, case



router = APIRouter(
    prefix="/catalog",
    tags=["catalog"],
)


@router.get("/")
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
            if item.quantity > 0:
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


@router.get("/recs")
def get_recs(userId: int):
    """
    REQ:
        {
        "userId": "integer"
        }
    RES:
        [{
            "productID": "integer",
            "product_name": "string",
            "category": "string",
            "sale price": "integer",
            "rental price": "integer",
            "stock": "integer",
            "description": "string"
        }]
    """
    cat = []
    categories = {}

    with db.engine.begin() as connection:
        # get cart item entries for the user in the past month
        carts = connection.execute(sqlalchemy.text("""SELECT c.id, ci.product_id, ci.quantity, ci.price, p.name, p.category_id
                                                   FROM carts as c
                                                   JOIN cart_items as ci on ci.cart_id = c.id
                                                   JOIN products as p on p.id = ci.product_id
                                                   WHERE c.user_id = :user_id and c.created_at >= CURRENT_DATE - INTERVAL '31 days'"""),
                                                   [{
                                                       "user_id": userId
                                                   }]).fetchall()
        
        if carts == []:
            # just give them the normal catalog...
            print("nothing bought before...")
            return get_catalog()
        
        category_rows = connection.execute(sqlalchemy.text("""SELECT id
                                                           FROM categories""")).fetchall()
        for i in category_rows:
            categories[i.id] = 0

        for cart in carts:
            current_cart = cart.id 
            current_item = cart.product_id
            print("current cart: ", current_cart)
            print("current product_id: ", current_item, " ", cart.name, " ", cart.category_id)
            categories[cart.category_id] = categories[cart.category_id] + 1

        print(categories)

        sorted_categories = [k for k, v in sorted(categories.items(), key=lambda item: item[1], reverse=True)]
        print(sorted_categories)

        # Create a CASE statement for custom ordering
        case_order = case(
            {value: index + 1 for index, value in enumerate(sorted_categories)},
            value=db.products.c.category_id,
            else_=len(sorted_categories) + 1
        )

        stmt = (
            sqlalchemy.select(
                db.products.c.id,
                db.products.c.name,
                db.products.c.description,
                func.sum(db.stock_ledger.c.change).label('quantity'),
                db.products.c.sale_price,
                db.products.c.daily_rental_price,
                db.categories.c.type
            ).select_from(
                db.stock_ledger
                    .join(db.products, db.products.c.id == db.stock_ledger.c.product_id)
                    .join(db.categories, db.products.c.category_id == db.categories.c.id)
            ).group_by(
                db.products.c.id,
                db.products.c.name,
                db.products.c.description,
                db.products.c.sale_price,
                db.products.c.daily_rental_price,
                db.categories.c.type
            ).order_by(
                case_order
            )
        )

        result = connection.execute(stmt).fetchall()

        print(result)

    for item in result:
        if item.quantity > 0:
            cat.append(
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

            

    return cat