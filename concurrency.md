# Concurency Issues

## 1.Two users (User A and User B) are making wholesale purchase plans concurrently.

  ### Initial State:

  money_ledger shows a total of $1000.
  products table shows sku "A001" has a quantity of 10 units at $50 each.
  
  ### Concurrent Execution
  
  User A's Request: 
  - Reads total money available: $1000.
  - Decides to buy 20 units of sku "A001" (20 * $50 = $1000).
  - Updates stock and money ledger.
  
  User B's Request (almost simultaneously):
  - Reads total money available: $1000.
  - Also decides to buy 20 units of sku "A001" (20 * $50 = $1000).
  - Updates stock and money ledger.
  
  Outcome: Both requests think they have $1000 available and proceed with their plans, leading to:
  - An overspend as they both "spend" $1000.
  - Inconsistent stock levels since both think they can buy 20 units of the same item, leading to potential stock levels dropping below zero or inaccurate stock records.
  
  Solution: To mitigate these concurrency issues, you can employ database transactions and locks to ensure that the shared resources are updated atomically. 
  - Use Transactions
  - Wrap the entire operation of reading the balance, deciding on purchases, and updating the ledger within a single database transaction.
  - Use Locks
  - Apply FOR UPDATE locks when querying the balance and stock levels to ensure no other transaction can modify these records until the current transaction is complete.

## 2. Checkout Process Race Conditions
  ### Initial State:
  
  User: User with userID = 1
  Cart: Cart with cartID = 100
  - Product A (productID = 200): quantity 5, price $10 each
  - Product B (productID = 300): quantity 3, price $15 each
  
  Stock Levels:
    Product A: 20 units
    Product B: 10 units
    
  Money Ledger:
  Total money: $1000
  
  ### Concurrent Execution
  
  Request A:
  - Reads Cart Items: 5 units of Product A, 3 units of Product B.
  - Processes Checkout:
    Subtracts 5 units of Product A (new stock: 15 units).
    Subtracts 3 units of Product B (new stock: 7 units).
    Adds $95 to money ledger (new total: $1095).
  
  Request B (almost simultaneously):
  - Reads Cart Items: 5 units of Product A, 3 units of Product B.
  - Processes Checkout:
    Subtracts another 5 units of Product A (new stock: 10 units).
    Subtracts another 3 units of Product B (new stock: 4 units).
    Adds another $95 to money ledger (new total: $1190).
    
  ### Outcome:
  
  Stock Levels: Incorrectly decremented twice.
  Product A: Final stock 10 units (expected 15).
  Product B: Final stock 4 units (expected 7).
  Money Ledger: Incorrectly added $95 twice (total: $1190, expected $1095).
  
  ### Solution: Use transactions and locks.
  
  Use Transactions
  Wrap the entire operation of reading the cart, updating stock, and ledger within a single database transaction.
  
  Use Locks
  Apply FOR UPDATE locks when querying cart items to ensure no other transaction can modify these records until the current transaction is complete.


