from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/reset")
def reset():
    """
    TEST....
    """
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(        """
        CREATE TABLE test (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            age INTEGER
        );
        """))


                 
    return "OK"

