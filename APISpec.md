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
    "productID": "int",
    "product_name": "string",
    "price": "int",
    "stock": "int",
    "description": "string",
    "condition": "string"
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

### 1.3: Add item to cart - `/cart/{cartID}/product/{productID}`
**Request**:
```json
{
  "quantity": "int"
}
```

**Response**:
```json
{
  "success": "boolean"
}
```

### 1.4: Cart Checkout - `/cart/{cartID}` (POST)
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
### 2.1: Post item - `/marketplace/` (POST)
**Request**:
```json
{
  "productName": "int",
  "quantity": "int",
  "price": "int",
  "condition": "string",
  "description": "string"
}
```

**Response**:
```json
{
  "listingID": "int"
}
```

### 2.2: Sell item - `/marketplace/{listingID}` (POST)
**Request**:
```json
{
  "quantity": "int"
}
```

**Response**:
```json
{
  "item_sold": "string",
  "quantity": "int",
  "money_paid": "int"
}
```


## 3. User Registration
### 3.1: Register - `/cart/{cartID}` (POST) ``` this needs to be changed ```
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


## 4. Purchase New Stock

