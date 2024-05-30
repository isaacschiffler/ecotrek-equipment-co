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

    items = np.array(["tent", "backpack", "stove", "beanie", "cap", "t shirt", "chair", "sleeping bag", "boots", "jacket", "sandals", "socks", "water bottle"])

    sizes = np.array(["S", "M", "L"])

    products = []

    for i in range(0, 60):
        color = np.random.choice(colors).upper()
        item = np.random.choice(items).upper()
        size = np.random.choice(sizes).upper()
        sku = size + "_" + color + "_" + item
        name = color + " " + item
        if sku not in products:
            products.append(sku)
        else:
            i -= 1

    print(products)
    return
