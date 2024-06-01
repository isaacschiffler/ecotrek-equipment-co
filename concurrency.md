# Concurency Issues

1.Two users (User A and User B) are making wholesale purchase plans concurrently.

## Initial State:

money_ledger shows a total of $1000.
products table shows sku "A001" has a quantity of 10 units at $50 each.

## Concurrent Execution

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
