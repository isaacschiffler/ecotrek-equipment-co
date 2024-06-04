from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlalchemy
from sqlalchemy import text
from datetime import datetime, timedelta
from src import database as db
import time

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
    customer_id: int
    return_time: datetime

@router.post("/rent")
def rent_item(new_rental: NewRentalRequest):
    """
    Add New Rental Request

    Notes: 
    Same day (start day = end day) rental requests do not have up front fees attached.
    Rental requests exceeding one day will incur a product-specific fee x number of proposed rental days. This is a one time payment, non-refundable.
    If rental authorized, customer can rent proposed product of quantity one. Should the customer want to rent more, they complete a separate rental request. 

    Request:
    {
        "customer_id": "integer",
        "product_id": "integer",
        "start_time": "datetime",
        "end_time": "datetime"
    }
    Response:
    {   
        "Success": "boolean",
        "Message": "string",
        "Money paid": "integer"
    }
    """
    startTime = time.time()
    with db.engine.begin() as connection:
        # Check if customer exists
        customer = connection.execute(sqlalchemy.text("""
            SELECT id FROM users WHERE id = :customer_id
        """), {"customer_id": new_rental.customer_id}).fetchone()

        if customer is None:
            return {"success": False, "message": "Customer does not exist", "Money paid": 0}

        # Check if the product_id exists
        product = connection.execute(sqlalchemy.text("""
            SELECT id FROM products WHERE id = :product_id
        """), {"product_id": new_rental.product_id}).fetchone()

        if product is None:
            return {"success": False, "message": "Product does not exist", "Money paid": 0}

        # Validating end_time is after start_time
        if new_rental.end_time <= new_rental.start_time:
            return {"success": False, "message": "End time must be after start time", "Money paid": 0}

        # Validating stock to check if quantity of proposed rental item > 0
        quant = connection.execute(sqlalchemy.text("""
            SELECT SUM(change) FROM stock_ledger WHERE product_id = :product_id
        """), {"product_id": new_rental.product_id}).scalar()

        if quant <= 0:
            return {"success": False, "message": "Product out of stock. "}

        # Calculated up-front fee
        total_days = (new_rental.end_time - new_rental.start_time).days
        daily_rental_price = connection.execute(sqlalchemy.text("""
            SELECT daily_rental_price FROM products WHERE id = :id
        """), {
            "id": new_rental.product_id
        }).scalar()
        up_front_payment = total_days * daily_rental_price

        if (up_front_payment > 0):
            # Insert into processed table
            processed_id = connection.execute(sqlalchemy.text("""
                INSERT INTO processed (created_at, job_id, type)
                VALUES (:created_at, :job_id, :type)
                RETURNING id
            """), {
                "created_at": datetime.now(),
                "job_id": new_rental.customer_id,
                "type": "rental"
            }).scalar()

            # Update money ledger with up-front fee and foreign key reference to processed table
            connection.execute(sqlalchemy.text("""
                INSERT INTO money_ledger (change, description, trans_id)
                VALUES (:change, :description, :trans_id)
            """), {
                "change": up_front_payment,
                "description": "rental",
                "trans_id": processed_id
            })

             # Acceptable request: add rental to rentals
            connection.execute(sqlalchemy.text("""
                INSERT INTO rentals (customer_id, product_id, start_time, end_time)
                VALUES (:customer_id, :product_id, :start_time, :end_time)
            """), {
                'customer_id': new_rental.customer_id,
                'product_id': new_rental.product_id,
                'start_time': new_rental.start_time,
                'end_time': new_rental.end_time
            })

            # Update stock ledgers with temporary dip in product quantity
            connection.execute(sqlalchemy.text("""
                INSERT INTO stock_ledger (created_at, product_id, change, description, trans_id)
                VALUES (:created_at, :product_id, :change, :description, :trans_id)
            """), {
                'created_at': datetime.now(),
                'product_id': new_rental.product_id,
                'change': -1,
                'description': "Product temporarily being rented.",
                'trans_id': processed_id
            })

        else:
            # < 24 hours proposed, throw error
            return {"success": False, "message": "Rental periods must exceed 24 hours. "}

    endTime = time.time()
    print("TIMING:", endTime - startTime) 
    return {"success": True, "message": "Rental request added successfully", "Money paid": up_front_payment}

@router.post("/return")
def return_item(return_rental: ReturnRentalRequest):
    """
    Return Rental Item

    Notes: 
    All rentals returned after proposed end_date will be subject to a constant daily late fee ($20/day) following 24 hours of the due date (original end time).

    Request:
    {
        "rental_id": "integer",
        "customer_id": "integer"
        "return_time": "datetime"
    }

    Response:
    {
        "success": "boolean",
        "message": "string",
        "late_fee": "float"
    }
    """
    startTime = time.time()
    with db.engine.begin() as connection:
        rental = connection.execute(
            sqlalchemy.text("SELECT * FROM rentals WHERE id = :rental_id"),
            {"rental_id": return_rental.rental_id}
        ).fetchone()

        # Error handling
        if not rental:
            return {"success": False, "message": "Rental not found.", "late_fee": 0}

        if rental.return_time:
            return {"success": False, "message": "Item already returned.", "late_fee": 0}
        
        if rental.customer_id != return_rental.customer_id:
            return {"success": False, "message": "Invalid user for indicated rental return. "}

        # Insert transaction into processed table
        processed_id = connection.execute(sqlalchemy.text("""
            INSERT INTO processed (created_at, job_id, type)
            VALUES (:created_at, :job_id, :type)
            RETURNING id
        """), {
            "created_at": datetime.now(),
            "job_id": return_rental.rental_id,
            "type": "Rental Return"
        }).scalar()

        # Calculated late fee if applicable
        end_time = rental.end_time
        return_time_dt = return_rental.return_time
        
        if return_time_dt > end_time:
            late_days = (return_time_dt - end_time).days
            late_fee = late_days * DAILY_LATE_FEE

            if (late_fee > 0):
                # Insert money change from late fee into money ledger
                connection.execute(sqlalchemy.text("""
                    INSERT INTO money_ledger (change, description, trans_id)
                    VALUES (:change, :description, :trans_id)
                """), {
                    "change": late_fee,
                    "description": "Rental Late Fee",
                    "trans_id": processed_id
                })
        else:
            late_fee = 0

        connection.execute(
            sqlalchemy.text("""
                UPDATE rentals 
                SET return_time = :return_time, late_fee = :late_fee
                WHERE id = :rental_id
            """), {"return_time": return_rental.return_time, "late_fee": late_fee, "rental_id": return_rental.rental_id})

        # Increase stock for product by 1 since now returned.
        product_id = connection.execute(
            sqlalchemy.text("""SELECT product_id FROM rentals WHERE id = :id
            """), {"id": return_rental.rental_id}
        ).scalar()
        connection.execute(sqlalchemy.text("""
                INSERT INTO stock_ledger (created_at, product_id, change, description, trans_id)
                VALUES (:created_at, :product_id, :change, :description, :trans_id)
            """), {
                'created_at': datetime.now(),
                'product_id': product_id,
                'change': 1,
                'description': "Rented item returned.",
                'trans_id': processed_id
            })

    endTime = time.time()
    print("TIMING:", endTime - startTime) 
    return {"success": True, "message": "Item returned successfully", "late_fee": late_fee}
