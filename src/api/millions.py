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

router = APIRouter(
    prefix="/millions",
    tags=["millions"],
)

fake = Faker()

@router.post("/products")
def add_products():

    colors = np.array(["green", "blue", "red", "white", "black", "orange", "purple", "pink", "gray", "transparent"])

    cloth_items = np.array(["beanie", "cap", "t shirt", "jacket", "hoodie"])
    camp_items = np.array(["tent", "backpack", "stove", "chair", "sleeping bag", "water bottle"])
    foot_items = np.array(["socks", "boots", "sandals", "socks"])

    sizes = np.array(["S", "M", "L"])

    products = []

    with db.engine.begin() as connection:
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

@router.post("/stock_buy")
def buy_stock():
    return "OK"

@router.post("users")
def make_users():
    # probably like 100,000 users
    # each user has 2 carts?
    # each cart as 3-4 items?
    return "OK"
