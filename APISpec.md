# API Specification for Outdoor Equipment Shop and Exchange

## 1. Customer Purchasing/Renting

## 2. User Listing Item for Sale/Rent

## 3. User Registration

## 4. Audit Functions

## 5. Purchase New Stock

## 6. Customer Rating

## 7. Customer Return

## 8. Customer Trade-in

#1: Customer Purchasing/Renting
```json
{
  "accountID": "int",
  "orderID": "int",
  "productID": "int",
  "dateStart": "string",
  "dateEnd": "string"
}
```

#2: User Listing Itme for Sale/Rent
```json
{
  "productID": "int",
  "quantity": "int",
  "orderValue": "float",
  "condition: "string",
  "color: "string"
}
```
