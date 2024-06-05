## Peer Review Implemented Feedback

# Product Ideas
- Implemented suggested Renting endpoints including rental requests, returns, late fees, up-front fees, and appropriate stock shifts. (/src/api/rent.py)
- Added fluctuating prices depending on time of year (/src/api/catalog.py)
- Implemented reviews system (/src/api/catalog.py) and pagination.

# Code Review Feedback
- Combined list of connection.executes into single SQL query (admin.py)
- Removed * from query and stated explicitly what we are counting (carts.py)
- Used dictionaries {} rather than list of dictionaries [{}] in several endpoints that did not need the list
- To prevent concurrency issues, we directly updated quantity without selecting first (marketplace.py)
- preferred_activities: converted to string before stored in databse (users.py)
- Added error handling to check if phone/email already exists in database before inserting again. (users.py)
- Removed all instances of f-strings to ensure safety from data breaches
- Speed Optimization: Used "TRUNCATE" instead of "DELETE FROM" to reset tables
- Captitalized all SQL queries for ease in reuse.
- Combined using ".fetchone()[0]" to eliminate unnecessary variables (stock.py)
- Removed duplicate imports (users.py)
- Changed router.post to ("/user/") from "/user/{userID}"
- Added comments and docstrings with Requests and Response Headers
- Added new carts table column (checked_out) that is automatically set to False - gets set to True if hits /checkout


# API related feedback
- Made responses more consistent across endpoints(use format: "success" boolean, "message": string across several endpoints)
- Removed table "user" from schema.sql, and adjusted foreign key references accordingly.
- Combined initial insertions in schema.sql into one single statement per table
- Moved “INSERT INTO categories” statements to be before  “INSERT INTO products” statement. Important to ensure that the foreign key reference to categories table exists when creating products table entries.
- Moved “INSERT INTO processed” statement before  “INSERT INTO stock_ledger” statement. Same reason above.
- Given feedback that catalog can be very long with scale, we added filtering to catalog.
- changed /users/{userId} to /users/user for creating a new user.