import os
import dotenv
from sqlalchemy import create_engine, MetaData
import sqlalchemy
from fastapi import APIRouter
from datetime import date
from faker import Faker
import numpy as np
import random

def database_connection_url():
    dotenv.load_dotenv()

    return os.environ.get("POSTGRES_URI")

engine = create_engine(database_connection_url(), pool_pre_ping=True)

colors = ["GRN", "BLU", "RED", "WHT", "BLK", "ORNG", "PRPL", "PNK", "GRY", "NA"]

items = ["TENT", "BCKPK", "STOVE", "BEANIE", "CAP", "T-SHIRT", "CHAIR", "SLEEPING_BAG", "BOOTS", "JACKET", "SNDLS", "SOCKS", "WTR_BTTL"]

sizes = ["S", "M", "L"]

products = []

for i in range(0, 60):
    color = np.random.choice(colors)
    item = np.random.choice(items)
    size = np.random.choice(sizes)
