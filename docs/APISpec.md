# API Specification for Outdoor Equipment Shop and Exchange

## 1. Customer Purchasing
The API calls are made in this sequence when making a purchase:
1. `Get Catalog`
2. `New Cart`
3. `Add Item to Cart` (Can be called multiple times)
4. `Checkout Cart`

### 1.1: Get Catalog - `/catalog/` (GET)
**Response**:
```json
[
  {
    "productID": "integer",
    "product_name": "string",
    "category": "string",
    "sale price": "integer",
    "rental price": "integer",
    "stock": "integer",
    "description": "string"
  }
]
```

### 1.2: Create Cart - `/cart/` (POST)
**Request**:
```json
{
  "userID": "integer"
}
```

**Response**:
```json
{
  "cartID": "integer"
}
```

### 1.3: Add item to cart - `/cart/{cartID}/product/{productID}`
**Request**:
```json
{
  "quantity": "integer"
}
```

**Response**:
```json
{
  "success": "boolean"
}
```

### 1.4: Cart Checkout - `/cart/{cartID}/checkout` (POST)
**Request**:
```json
{
  "payment": "string"
}
```

**Response**:
```json
{
  "num_items_bought": "integer",
  "money_paid": "integer"
}
```

### 1.5: Catalog Recomendations - '/catalog/recs' (POST)
**Request**:
```json
{
  "userId": "integer"
}
```


**Response**:
```json
    [{
        "productID": "integer",
        "product_name": "string",
        "category": "string",
        "sale price": "integer",
        "rental price": "integer",
        "stock": "integer",
        "description": "string"
    }]
```

## 2. User Listing Item for Sale
### 2.1: Post item - `/marketplace/` (POST)
**Request**:
```json
{
  "productName": "string",
  "quantity": "integer",
  "price": "integer",
  "condition": "string",
  "description": "string"
}
```

**Response**:
```json
{
  "listingID": "integer"
}
```

### 2.2: Sell item - `/marketplace/{listingID}` (POST)
**Request**:
```json
{
  "quantity": "integer"
}
```

**Response**:
```json
{
  "item_sold": "string",
  "quantity": "integer",
  "money_paid": "integer"
}
```


## 3. User Registration
### 3.1: Register - `/user/{userID}` (POST)
Registering a new user into the database.

**Request**:
```json
{
  "name": "string",
  "email": "string",
  "phone_number": "string",
  "password": "string",
  "preferred_activities": ["string"]
}
```
**Response**:
```json
{
  "userID": "integer",
  "success": "boolean"
}
```

## 4. Purchase New Stock
### 4.1 Get Stock Purchase Plan - `/plan/` (GET)
Planning wholesale purchase plan
**Request**:
```json
[
  {
    "sku": "string",
    "category": "string",
    "price": "integer",
    "quantity": "integer"
  }
]
```
**Response**:
```json
[
    {
        "sku": "string", /* Must match a sku from the catalog just passed in this call */
        "quantity": "integer" /* A number between 1 and the quantity available for sale */
    }
]
```

### 4.2. Deliver Equipment Stock - `/stock/deliver/{orderID}
Buying items from wholesaler.
**Request**:
```json
[
  {
    "sku": "string",
    "category": "string",
    "price": "integer",
    "quantity": "integer"
  }
]
```

