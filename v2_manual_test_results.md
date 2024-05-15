# Flow 1
Alice has just discovered a hole in her backpack. She has a backpacking trip coming up so she needs to get a new one ASAP. First, Alice requests a catalog of backpacks that are offered by EcoTrek Equipment Co by calling GET /catalog/. She finds 5 different backpacks all at different prices. Being that she goes on backpacking trips often, she wants to purchase a more expensive, higher quality backpack. She then initiates a purchase of a backpack that costs $150. To do so she does the following:
* Call POST /users/user to create an account
* Call POST /carts/ to get a new cart with ID 333 
* Alice then calls POST /carts/333/product/NORTH_FACE_BACKPACK_32 and passes the quantity 1.
* Lastly, to checkout, she calls POST /carts/333/checkout to place her order. The checkout charges her $150 and sends her a backpack.
* Alice receives her backpack two days later at her door just in time for her trip.


Request:

curl -X 'GET' \
'https://ecotrek-equipment-co.onrender.com/catalog/' \
-H 'accept: application/json'

Response:
[
  {
    "productID": 9,
    "product_name": "North Face Backpack",
    "category": "Backpacking",
    "sale price": 150,
    "rental price": 15,
    "stock": 15,
    "description": "Perfect for backpacking and camping"
  },
  {
    "productID": 10,
    "product_name": "Wild Trek Backpack",
    "category": "Backpacking",
    "sale price": 45,
    "rental price": 5,
    "stock": 3,
    "description": "Large and great for camping"
  },
  {
    "productID": 7,
    "product_name": "Red Jansport Backpack",
    "category": "Backpacking",
    "sale price": 70,
    "rental price": 5,
    "stock": 10,
    "description": "Primarily for everyday use"
  },
  {
    "productID": 8,
    "product_name": "Green Patagonia Backpack",
    "category": "Backpacking",
    "sale price": 50,
    "rental price": 5,
    "stock": 5,
    "description": "Ideal for everyday use or hiking"
  },
  {
    "productID": 11,
    "product_name": "Blue Jansport Backpack",
    "category": "Backpacking",
    "sale price": 70,
    "rental price": 5,
    "stock": 2,
    "description": "Primarily for everyday use"
  }
]

Request:
curl -X 'POST' \
  'https://ecotrek-equipment-co.onrender.com/users/user/{userID}' \
  -H 'accept: application/json' \
  -H 'access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Alice",
  "email": "alice365@gmail.com",
  "phone_number": "8054555644",
  "preferred_activities": [
    "Hiking"
  ]
}'

Response:
{
  "userID": 1,
  "success": true
}


Request:
curl -X 'POST' \
  'https://ecotrek-equipment-co.onrender.com/carts/?userID=1' \
  -H 'accept: application/json' \
  -H 'access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0' \
  -d ''

Response:
{
  "cartID": 1
}


Request:
curl -X 'POST' \
  'https://ecotrek-equipment-co.onrender.com/carts/1/items/{productID}?product_id=5' \
  -H 'accept: application/json' \
  -H 'access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0' \
  -H 'Content-Type: application/json' \
  -d '{
  "quantity": 1
}'

Response:
“OK”


Request:
curl -X 'POST' \
  'https://ecotrek-equipment-co.onrender.com/carts/1/checkout' \
  -H 'accept: application/json' \
  -H 'access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0' \
  -H 'Content-Type: application/json' \
  -d '{
  "payment": "Discover Credit Card"
}'

Response:
{
  "num_items_bought": 1,
  "money_paid": 150
}


# Flow 2
John is an avid camper and in his many excursions amassed extra tents he no longer needs. He wants to sell one of his tents to give it to someone that can use it more than himself. First, John posts the item with the corresponding criteria for the listing by calling POST /marketplace/. The data passed to this POST endpoint includes relevant information about the product, including the product name, description, quantity, condition, and price. Now, other users are able to see John’s listing and can buy John’s blue tent using POST/marketplace{listingId}.
* First, John calls POST /marketplace/ to create a new listing with ID 2. John's item (with name= “blue tent”, condition= “good”, quantity= 1, price= 100, description= “small 2-person tent”) is listed on the website for people to see and potentially purchase.
* Alice buys an item on the marketplace with Id 2 (John’s blue tent), calling POST /marketplace/2 with quantity 1. She spends money=100 and gets 1 tent in return. The total quantity on John’s listing is now 0 as a result.


Request:
curl -X 'POST' \
  'http://127.0.0.1:8000/marketplace/marketplace' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "productName": "Blue Tent",
  "quantity": 1,
  "price": 100,
  "condition": "good",
  "description": "small 2-person tent"
}'

Response:

{
  "listingID": 2
}


Request:
curl -X 'POST' \
  'http://127.0.0.1:8000/marketplace/marketplace/2?quantity=1' \
  -H 'accept: application/json' \
  -d ''

Response:

{
  "item_sold": "Blue Tent",
  "quantity": 1,
  "money_paid": 100
}




# Flow 3
Our shop has recently sold lots of items and needs to restock to make sure we have supply to fulfill demands. Thus we want to purchase more The North Face jackets and tents.
* First, we call GET /plan to receive the wholesale catalog that The North Face offers. We will go through this catalog to find jackets and tents that we need to restock.
* Then, after submitting our plan, the supplier calls POST /stock/deliver/{orderID} in which we may for the order and receive our purchase plan. We add our new stock to the catalog we offer.

Request:
curl -X 'POST' \
  'http://127.0.0.1:8000/stock/plan' \
  -H 'accept: application/json' \
  -H 'access_token: 6504e9c07a7c552a0eaf5282bbca2047' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "sku": "YELLOW_SOCK",
    "category_id": 1,
    "price": 5,
    "quantity": 100
  }
]'

Response:
[
  {
    "sku": "YELLOW_SOCK",
    "quantity": 50,
    "price": 5,
    "category_id": 1
  }
]


Request:
curl -X 'POST' \
  'http://127.0.0.1:8000/stock/deliver/1' \
  -H 'accept: application/json' \
  -H 'access_token: 6504e9c07a7c552a0eaf5282bbca2047' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "sku": "YELLOW_SOCK",
    "quantity": 10,
    "price": 5,
    "category_id": 1
  }
]'

Response:
"OK"

