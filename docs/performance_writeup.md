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
