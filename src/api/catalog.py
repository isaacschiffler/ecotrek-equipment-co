import sqlalchemy
from src import database as db
from fastapi import APIRouter
from sqlalchemy.sql import select, func, case
from datetime import date
import time


router = APIRouter(
    prefix="/catalog",
    tags=["catalog"],
)


@router.get("/")
def get_catalog():
    startTime = time.time()
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
                rating = connection.execute(sqlalchemy.text("SELECT avg(rating) FROM reviews where product_id = :pid"), {'pid': item.id}).fetchone()[0]
        
                # create a factor to scale up or down the price based on how well the product is rated
                pricingFactor = 1
                if rating is not None:
                    pricingFactor -= (float(rating) - 3) / 20
                
                currentMonth = date.today().strftime("%B")

                # discounting backpacking equipment in ceratin months
                if item.type == "BACKPACKING" and currentMonth in ['April', 'May', 'June']:
                        pricingFactor -= 0.1
                
                # increasing the price of shelter for peak times
                if item.type == "SHELTER" and currentMonth in ['October', 'November', 'December', "January"]:
                        pricingFactor += 0.05

                print("final pricing factor:", pricingFactor)
                print("original sale price:", item.sale_price)
                catalog.append(
                    {
                        "productID": item.id,
                        "product_name": item.name,
                        "category": item.type,
                        "sale price": round(item.sale_price * pricingFactor, 2),
                        "rental price": item.daily_rental_price,
                        "stock": item.quantity,
                        "description": item.description
                    }
                )
    endTime = time.time()
    print("TIMING:", endTime - startTime)
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
    startTime = time.time()
    cat = []
    categories = {}
    money_spends = {}

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
            categories[cart.category_id] = categories[cart.category_id] + 1 * cart.quantity

        print(categories)

        sorted_categories = [k for k, v in sorted(categories.items(), key=lambda item: item[1], reverse=True)]
        print(sorted_categories)

        # get money spent for past orders
        moneys = connection.execute(sqlalchemy.text("""SELECT m.change as total, ci.price as unit_price, ci.quantity as quantity
                                                    FROM processed as p
                                                    JOIN money_ledger as m on m.trans_id = p.id
                                                    JOIN carts as c on c.id = p.job_id
                                                    JOIN cart_items as ci on ci.cart_id = c.id
                                                    WHERE c.user_id = :user_id"""),
                                                    [{
                                                        'user_id': userId
                                                    }]).fetchall()
        
        for trans in moneys:
            money_spends[trans.unit_price] = money_spends.get(trans.unit_price, 0) + trans.quantity

        sorted_spends = [k for k, v in sorted(money_spends.items(), key=lambda item: item[1], reverse=True)]
        print(sorted_spends)
            

        # Create a CASE statement for custom ordering
        case_categories = case(
            {value: index + 1 for index, value in enumerate(sorted_categories)},
            value=db.products.c.category_id,
            else_=len(sorted_categories) + 1
        )

        case_spends = case(
            {value: index + 1 for index, value in enumerate(sorted_spends)},
            value=db.products.c.sale_price,  # Assuming sale_price is the unit_price equivalent
            else_=len(sorted_spends) + 1
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
                case_categories,
                case_spends
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

    endTime = time.time()
    print("TIMING:", endTime - startTime)

    return cat


@router.post("/review")
def add_review(userId: int, productId: int, rating: int, description: str):
    """
    Add reviews for a product

    REQ:
        {
        "userId": "integer",
        "productId": "integer"
        }
    RES:
        {
        "success": "boolean",
        "error": "string"
        }
    """
    startTime = time.time()
    
    with db.engine.begin() as connection:

        if rating < 0 or rating > 5:
            return {"success": False, "error": "rating must be between 0 and 5"}

        user_exists = connection.execute(
            sqlalchemy.text("SELECT 1 FROM users WHERE id = :userId"),
            {'userId': userId}
        ).scalar()

        product_exists = connection.execute(
            sqlalchemy.text("SELECT 1 FROM products WHERE id = :productId"),
            {'productId': productId}
        ).scalar()

        if not product_exists or not user_exists:
            return {"success": False, "message": "Invalid product or user passed. "}

        connection.execute(sqlalchemy.text("""
                                            INSERT INTO reviews (product_id, customer_id, rating, description)
                                            VALUES (:pid, :uid, :rating, :desc);
                                            """), {'pid': productId, 'uid': userId, 'rating': rating, 'desc': description})
    endTime = time.time()
    print("TIMING:", endTime - startTime)
    return {"success": True, "error": "none"}


@router.get("/search")
def search_reviews(productId: int, displayLimit: int = 10, keywords : str = "", rating: int = -1):
    """
    Search through reviews based on keywords or rating

    REQ:
        {
        "productId": "integer",
        "displayLimit": "integer",
        "keywords": "string",
        "rating": "integer"
        }
    RES:
        [{
            "name": "string",
            "rating": "integer",
            "description": "string"
        }]
    """
    startTime = time.time()
    with db.engine.begin() as connection:
        product_exists = connection.execute(
            sqlalchemy.text("SELECT 1 FROM products WHERE id = :product_id"),
            {'product_id': productId}
        ).scalar()

        if not product_exists:
            return {"success": False, "message": "product Does not exist."}

        stmt = (
            sqlalchemy.select(
                db.products.c.name,
                db.reviews.c.rating,
                db.reviews.c.description
            )
            .limit(displayLimit)
            .select_from(
                db.reviews
                .join(db.products, db.products.c.id == db.reviews.c.product_id)
            )
            .where(db.reviews.c.description.like(f"%{keywords}%"))
        )

        if rating != -1:
            stmt = stmt.where(db.reviews.c.rating == rating)
        
        result = connection.execute(stmt).fetchall()
        retVal = []

        for item in result:
            retVal.append(
                {
                    "name": item.name,
                    "rating": item.rating,
                    "description": item.description
                }
            )
    endTime = time.time()
    print("TIMING:", endTime - startTime)
    return retVal