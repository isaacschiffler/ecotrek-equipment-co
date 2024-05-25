import os
import dotenv
from sqlalchemy import create_engine
import sqlalchemy

def database_connection_url():
    dotenv.load_dotenv()

    return os.environ.get("POSTGRES_URI")

engine = create_engine(database_connection_url(), pool_pre_ping=True)
# create tables in metadata
metadata_obj = sqlalchemy.MetaData()


processed = sqlalchemy.Table("processed", metadata_obj, autoload_with=engine)
users = sqlalchemy.Table("users", metadata_obj, autoload_with=engine)
categories = sqlalchemy.Table("categories", metadata_obj, autoload_with=engine)
products = sqlalchemy.Table("products", metadata_obj, autoload_with=engine)
money_ledger = sqlalchemy.Table("money_ledger", metadata_obj, autoload_with=engine)
stock_ledger = sqlalchemy.Table("stock_ledger", metadata_obj, autoload_with=engine)
carts = sqlalchemy.Table("carts", metadata_obj, autoload_with=engine)
cart_items = sqlalchemy.Table("cart_items", metadata_obj, autoload_with=engine)
marketplace = sqlalchemy.Table("marketplace", metadata_obj, autoload_with=engine)