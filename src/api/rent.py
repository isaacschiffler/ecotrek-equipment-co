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

LATE_FEE_PER_HOUR = 10

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
        "message": "string"
    }
    """
    with db.engine.begin() as connection:
        
        connection.execute(sqlalchemy.text("""
            INSERT INTO rentals (customer_id, product_id, start_time, end_time)
            VALUES (:customer_id, :product_id, :start_time, :end_time)
        """), {
            'customer_id': new_rental.customer_id,
            'product_id': new_rental.product_id,
            'start_time': new_rental.start_time,
            'end_time': new_rental.end_time
        })
    return {"message": "Rental request added successfully"}

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
        "message": "string",
        "late_fee": "float"
    }
    """
    with db.engine.begin() as connection:
        rental = connection.execute(
            text("SELECT * FROM rentals WHERE id = :rental_id"),
            {"rental_id": return_rental.rental_id}
        ).fetchone()

        if not rental:
            raise HTTPException(status_code=404, detail="Rental not found")

        if rental.return_time:
            raise HTTPException(status_code=400, detail="Item already returned")

        # Calculate late fee if applicable
        end_time = rental.end_time
        return_time_dt = return_rental.return_time
        if return_time_dt > end_time:
            late_hours = (return_time_dt - end_time).total_seconds() / 3600
            late_fee = late_hours * LATE_FEE_PER_HOUR
        else:
            late_fee = 0

        connection.execute(
            text("""
                UPDATE rentals 
                SET return_time = :return_time, late_fee = :late_fee
                WHERE id = :rental_id
            """), {"return_time": return_rental.return_time, "late_fee": late_fee, "rental_id": return_rental.rental_id})

    return {"message": "Item returned successfully", "late_fee": late_fee}
