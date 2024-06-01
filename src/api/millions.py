from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
from enum import Enum
import sqlalchemy
from src import database as db
from fastapi import APIRouter
from datetime import date
from faker import Faker
import numpy as np
import random
from src.api import stock

router = APIRouter(
    prefix="/millions",
    tags=["millions"],
)

fake = Faker()

def add_products():

    colors = np.array(["green", "blue", "red", "white", "black", "orange", "purple", "pink", "gray", "transparent"])

    cloth_items = np.array(["beanie", "cap", "t shirt", "jacket", "hoodie"])
    camp_items = np.array(["tent", "backpack", "stove", "chair", "sleeping bag", "water bottle"])
    foot_items = np.array(["socks", "boots", "sandals", "socks"])

    sizes = np.array(["S", "M", "L"])

    products = []

    with db.engine.begin() as connection:
        # add lots of cash...
        connection.execute(sqlalchemy.text("""INSERT INTO money_ledger (change, description)
                                           VALUES (30000000, 'lots of money to simulate with...')"""))
        # clothing proudcts
        id = connection.execute(sqlalchemy.text("""SELECT id
                                                          FROM categories
                                                          WHERE type = 'CLOTHING'""")).fetchone()[0]
        for i in range(0, 20):
            color = np.random.choice(colors).upper()
            item = np.random.choice(cloth_items).upper()
            size = np.random.choice(sizes).upper()
            sku = size + "_" + color + "_" + item.replace(' ', '_')
            name = color + " " + item
            rent_price = np.random.randint(5, 15)
            sale_price = np.random.randint(25, 100)
            descr = "Very high quality, comfy, and soft " + name.lower()
            item = {
                "sku": sku,
                "name": name,
                "description": descr,
                "cat_id": id,
                "sale_price": sale_price,
                "rent_price": rent_price
            }
            if item not in products:
                products.append(item)
            else:
                i -= 1

        # camp product
        id = connection.execute(sqlalchemy.text("""SELECT id
                                                          FROM categories
                                                          WHERE type = 'BACKPACKING'""")).fetchone()[0]
        for i in range(0, 30):
            color = np.random.choice(colors).upper()
            item = np.random.choice(camp_items).upper()
            size = np.random.choice(sizes).upper()
            sku = size + "_" + color + "_" + item.replace(' ', '_')
            name = color + " " + item
            sale_price = np.random.randint(50, 200)
            rent_price = np.random.randint(5, 15)
            descr = "Very useful and practical " + name.lower()
            item = {
                "sku": sku,
                "name": name,
                "description": descr,
                "cat_id": id,
                "sale_price": sale_price,
                "rent_price": rent_price
            }
            if item not in products:
                products.append(item)
            else:
                i -= 1

        #footwear products
        id = connection.execute(sqlalchemy.text("""SELECT id
                                                          FROM categories
                                                          WHERE type = 'CLOTHING'""")).fetchone()[0]
        for i in range(0, 15):
            color = np.random.choice(colors).upper()
            item = np.random.choice(foot_items).upper()
            size = np.random.choice(sizes).upper()
            sku = size + "_" + color + "_" + item.replace(' ', '_')
            name = color + " " + item
            sale_price = np.random.randint(20, 100)
            rent_price = np.random.randint(5, 15)
            descr = "Very comfortable and lasting " + name.lower()
            item = {
                "sku": sku,
                "name": name,
                "description": descr,
                "cat_id": id,
                "sale_price": sale_price,
                "rent_price": rent_price
            }            
            if item not in products:
                products.append(item)
            else:
                i -= 1
    
        # insert the products into the products table
        connection.execute(sqlalchemy.text("""INSERT INTO products (sku, name, description, category_id, sale_price, daily_rental_price)
                                           VALUES (:sku, :name, :description, :cat_id, :sale_price, :rent_price)"""),
                                           products)

    return products

class Stock(BaseModel):
    sku: str
    category_id: int
    price: int
    quantity: int

@router.post("/stock_buy")
def buy_stock():
    product_list = add_products()
    print("products added...")
    buy_plan = []
    for i in product_list:
        buy_plan.append(Stock(
            sku=i["sku"],
            category_id=i["cat_id"],
            price=round(i["sale_price"] * (1 / 1.2), 2),
            quantity=4000
        ))
    stock.post_deliver_stock(buy_plan, 1)
    print("products bought and delivered...")
    return "OK"

@router.post("/users")
def make_users():
    # probably like 100,000 users
    # each user has 2 carts?
    # each cart as 3-4 items?

    # initiate product fake data
    buy_stock()

    users = []

    possible_activities = ["Hiking", "Camping", "Running", "Cooking", "Backpacking", "Hunting", "Fishing"]

    for i in range(0, 100000):
        name = fake.name()
        email = fake.email()
        number = random.randint(1000000000, 9999999999) # using this for phone number instead of fake.phone_number() b/c the database was set to int8 not text
        activities = random.sample(possible_activities, 3)
        users.append({
            "name": name,
            "email": email,
            "number": number,
            "activities": activities
        })
    print("100,000 users generated")
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""INSERT INTO users (name, email, phone_number, preferred_activities)
                                           VALUES (:name, :email, :number, :activities)"""),
                                           users)
    print("100,000 users inserted")

    #create carts for each user
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""INSERT INTO carts (user_id)
                                           SELECT id
                                           FROM users"""))
        connection.execute(sqlalchemy.text("""INSERT INTO carts (user_id)
                                           SELECT id
                                           FROM users"""))
    print("200,000 total carts created")

    #add items to each cart
    with db.engine.begin() as connection:
        for j in range(0, 3):
            for i in range(9, 74):
                print("added product ", i, " to carts")
                cart_id_high = ((i + j - 8) * 3333) % 200000
                cart_id_low = ((i + j - 9) * 3333) % 200000
                rand_quant = random.randint(1, 3)
                connection.execute(sqlalchemy.text("""INSERT INTO cart_items (cart_id, product_id, quantity, price)
                                                SELECT c.id as cart_id, p.id as product_id, :rand_num, p.sale_price
                                                FROM carts as c
                                                JOIN products as p on p.id = :prod_id
                                                WHERE c.id > :low and c.id <= :high
                                                """),
                                                [{
                                                    "rand_num": rand_quant,
                                                    "prod_id": i,
                                                    "low": cart_id_low,
                                                    "high": cart_id_high
                                                }])
    print("over 630,000 items added to carts")

    # now checkout for them all... definitely gonna be well over 1M, maybe just do 2 items per cart above?^^^^^

    return "OK"
