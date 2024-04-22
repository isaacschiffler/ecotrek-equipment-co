# API Specification for Outdoor Equipment Shop and Exchange

## 1. Customer Purchasing
### 1.1: Get Catalog - `/catalog/` (GET)
**Response**:
```json
[
  {
    "productID": "int",
    "product_name": "string",
    "price": "int",
    "stock": "int",
    "description": "string",
    "quality": "string"
  }
]
```

### 1.2: Create Cart - `/cart/` (POST)
**Request**:
```json
{
  "customerID": "int"
}
```

**Response**:
```json
{
  "cartID": "int"
}
```

### 1.3: Cart Checkout - `/cart/{cartID}` (POST)
**Request**:
```json
{
  "payment": "string"
}
```

**Response**:
```json
{
  "num_items_bought": "int",
  "money_paid": "int"
}
``` 

## 2. User Listing Item for Sale
### 2.1: CHANGE THIS TO MATCH PROF FORMATTING
```json
{
  "productID": "int",
  "quantity": "int",
  "orderValue": "float",
  "condition": "string",
  "color": "string"
}
```

## 3. User Registration
### 3.1: Register - `/cart/{cartID}` (POST)
**Request**:
```json
{
  "name": "string",
  "email": "string",
  "password": "string",
  "location": "string",
  "preferred_activities": ["string"]
}
```

## 4. Audit Functions
### 3.1: Stock - `/cart/{cartID}` (POST)
**Response**:
```json
[
  {
    "activity": "string",
    "item_type": "string",
    "quantity_in_stock": "string",
    "quantity_on_loan": "string"
  }
]
```

## 5. Purchase New Stock

## 6. Customer Rating

## 7. Customer Return

## 8. Customer Trade-in
