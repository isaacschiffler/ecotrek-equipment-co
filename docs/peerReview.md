## Peer Review Implemented Feedback

# Product Ideas
- Implemented suggested Renting endpoints (/src/api/rent.py)
- Added fluctuating prices depending on time of year (/src/api/catalog.py)
- Implemented reviews system (/src/api/catalog.py)

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

# API related feedback