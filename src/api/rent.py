from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlalchemy
from sqlalchemy import text
from datetime import datetime, timedelta
from src import database as db

router = APIRouter(
    prefix="/rentals",
    tags=["rentals"],
)

DAILY_LATE_FEE = 20

class NewRentalRequest(BaseModel):
    customer_id: int
    product_id: int
    start_time: datetime
    end_time: datetime

class ReturnRentalRequest(BaseModel):
    rental_id: int
    return_time: datetime

@router.post("/rent")
def rent_item(new_rental: NewRentalRequest):
    """
    Add New Rental Request
    Request:
    {
        "customer_id": "integer",
        "product_id": "integer",
        "start_time": "datetime",
        "end_time": "datetime"
    }
    Response:
    {   
        "success": "boolean",
        "message": "string"
    }
    """
    with db.engine.begin() as connection:
        # Check if customer exists
        customer = connection.execute(text("""
            SELECT id FROM users WHERE id = :customer_id
        """), {"customer_id": new_rental.customer_id}).fetchone()

        if customer is None:
            return {"success": False, "message": "Customer does not exist"}

        # Check if the product_id exists
        product = connection.execute(text("""
            SELECT id FROM products WHERE id = :product_id
        """), {"product_id": new_rental.product_id}).fetchone()

        if product is None:
            return {"success": False, "message": "Product does not exist"}

        # Validating end_time is after start_time
        if new_rental.end_time <= new_rental.start_time:
            return {"success": False, "message": "End time must be after start time"}


        # Acceptable request
        connection.execute(sqlalchemy.text("""
            INSERT INTO rentals (customer_id, product_id, start_time, end_time)
            VALUES (:customer_id, :product_id, :start_time, :end_time)
        """), {
            'customer_id': new_rental.customer_id,
            'product_id': new_rental.product_id,
            'start_time': new_rental.start_time,
            'end_time': new_rental.end_time
        })
    
    return {"success": True, "message": "Rental request added successfully"}

@router.post("/return")
def return_item(return_rental: ReturnRentalRequest):
    """
    Return Rental Item

    Request:
    {
        "rental_id": "integer",
        "return_time": "datetime"
    }

    Response:
    {
        "success": "boolean",
        "message": "string",
        "late_fee": "float"
    }
    """
    with db.engine.begin() as connection:
        rental = connection.execute(
            text("SELECT * FROM rentals WHERE id = :rental_id"),
            {"rental_id": return_rental.rental_id}
        ).fetchone()

        # Error handling
        if not rental:
            return {"success": False, "message": "Rental not found.", "late_fee": 0}

        if rental.return_time:
            return {"success": False, "message": "Item already returned", "late_fee": 0}

        # Calculated late fee if applicable
        end_time = rental.end_time
        return_time_dt = return_rental.return_time
        if return_time_dt > end_time:
            late_days = (return_time_dt - end_time).days
            late_fee = late_days * DAILY_LATE_FEE
        else:
            late_fee = 0

        connection.execute(
            text("""
                UPDATE rentals 
                SET return_time = :return_time, late_fee = :late_fee
                WHERE id = :rental_id
            """), {"return_time": return_rental.return_time, "late_fee": late_fee, "rental_id": return_rental.rental_id})

    return {"success": True, "message": "Item returned successfully", "late_fee": late_fee}
