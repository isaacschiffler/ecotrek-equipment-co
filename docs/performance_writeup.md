# Fake Data Modeling
millions.py file in src/api (can be run directly from render endpoints (please don't though))
Each table has the following row counts
- users: 200k
- carts: 200k
- cart_items: 213k
- reviews: 38k
- processed: 200k
- stock_ledger: 213k
- money_ledger: 200k
- products: 138
- marketplace: 300

I chose this distribution because I thought that for the most part, each user/customer would only place one order with us (at least in a short time period) and each cart for the customer would on average contain just over 1 item, so there are 13k more entries in cart_items than carts. Furthermore, most people would not leave reviews, so there are only 25k reviews. For each customer purchase, an entry is made into money_ledger, processed, and money_ledger (some depend on carts, some depend on cart_items). Furthermore, there aren't a ton of products or marketplace listings compared to the rest of tables because direct customer sales are the most common use of our store.


# Performance Improvements
Time for each endpoint:
- /users/user/ - 121ms
- /catalog/ - 1873ms
- /catalog/recs - 371ms
- /catalog/review - 123ms
- /catalog/search - 94ms
- /carts/ - 104ms
- /carts/{cart_id}/items/{productID} - 157ms
- /carts/{cart_id}/checkout - 248ms
- /rentals/rent - 115ms
- /rentals/return - 98ms
- /stock/plan - 106ms
- /stock/deliver/{order_id} - 84ms


Slowest endpoints:

/catalog/ 
The query planner indicates that it is doing a sequential scan. 
Adding an index on the type in categories (which is part of the group by) helps significantly with the performance of the longer query.
The final time for the endpoint was 1489ms.

/catalog/recs
The query planner indicates that it is doing multiple sequential scans and uses a few of the indexes based on the primary keys.
Adding an index on user_id in carts improved its time by around 7x.
The final time for the endpoint was 295ms.

/carts/{cart_id}/checkout
The query planner says that it is doing a sequential scan for the main query.
An index on trans_id in stock_ledger helps significantly with the performance.
The final time for the endpoint was 125ms.
