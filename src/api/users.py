from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from sqlalchemy.sql import func
from sqlalchemy import text
from src import database as db
from enum import Enum
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

class PreferredActivity(str, Enum):
    Hiking = "Hiking"
    Camping = "Camping"
    Running = "Running"
    Cooking = "Cooking"
    Backpacking = "Backpacking"
    Hunting = "Hunting"
    Fishing = "Fishing"

class User(BaseModel):
    name: str
    email: str
    phone_number: str
    preferred_activities: List[PreferredActivity]


@router.post("/user/")
def user_register(newUser: User):
    """
    REQ
        {
        "name": "string",
        "email": "string",
        "phone_number": int,
        "preferred_activities": List[PreferredActivity]
        }
    RES
        {
        "userID": "integer",
        "success": "boolean"
        }

    """

    with db.engine.begin() as connection:
        # converting enum to str when add to table
        preferred_activities_str = ','.join(activity.value for activity in newUser.preferred_activities)
        preferred_activities_str = "{" + preferred_activities_str + "}"

        email_check = text("SELECT id FROM users WHERE email = :email")
        phone_check = text("SELECT id FROM users WHERE phone_number = :phone_number ")
        existing_email = connection.execute(email_check, {"email": newUser.email}).scalar()
        existing_phone = connection.execute(phone_check, {"phone_number": newUser.phone_number}).scalar()


        if existing_email or existing_phone:
            # email or phone number already exist in table, avoiding duplicate rows
            return {"userID": None, "success": False, "message": "Email and/or Phone Number already exists"}
        
        userID = connection.execute(
            sqlalchemy.text("INSERT INTO users (name, email, phone_number, preferred_activities) "
                            "VALUES (:name, :email, :phone_number, :preferred_activities) RETURNING id"),
                            {"name": newUser.name,
                             "email": newUser.email,
                            "phone_number": newUser.phone_number, 
                            "preferred_activities": preferred_activities_str}).scalar_one()
    
        print("Creating user for {} with id {}".format(newUser.name, userID))

        if (userID):
            success = True
        else:
            success = False

        return {"userID": userID, "success": success}
