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


colors = ["green", "blue", "red", "white", "black", "orange", "purple", "pink", "gray", "transparent"]

items = ["tent", "backpack", "stove", "beanie", "cap", "t shirt", "chair", "sleeping bag", "boots", "jacket", "sandals", "socks", "water bottle"]

sizes = ["S", "M", "L"]

products = []

for i in range(0, 60):
    color = np.random.choice(colors)
    item = np.random.choice(items)
    size = np.random.choice(sizes)
    products += size.upper() + "_"

print(products)
