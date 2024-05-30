from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
from enum import Enum
import sqlalchemy
from fastapi import APIRouter
from datetime import date
from faker import Faker
import numpy as np
import random

router = APIRouter(
    prefix="/millions",
    tags=["millions"],
)


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
                                                          WHERE type = CLOTHING""")).fetchone()[0]
        for i in range(0, 20):
            color = np.random.choice(colors).upper()
            item = np.random.choice(cloth_items).upper()
            size = np.random.choice(sizes).upper()
            sku = size + "_" + color + "_" + item
            name = color + " " + item
            if sku not in products:
                products.append(sku)
            else:
                i -= 1

        # camp product
        id = connection.execute(sqlalchemy.text("""SELECT id
                                                          FROM categories
                                                          WHERE type = BACKPACKING""")).fetchone()[0]
        for i in range(0, 30):
            color = np.random.choice(colors).upper()
            item = np.random.choice(camp_items).upper()
            size = np.random.choice(sizes).upper()
            sku = size + "_" + color + "_" + item
            name = color + " " + item
            if sku not in products:
                products.append(sku)
            else:
                i -= 1

        #footwear products
        id = connection.execute(sqlalchemy.text("""SELECT id
                                                          FROM categories
                                                          WHERE type = CLOTHING""")).fetchone()[0]

        for i in range(0, 15):
            color = np.random.choice(colors).upper()
            item = np.random.choice(foot_items).upper()
            size = np.random.choice(sizes).upper()
            sku = size + "_" + color + "_" + item
            name = color + " " + item
            if sku not in products:
                products.append(sku)
            else:
                i -= 1
    

    print(products)
    return
