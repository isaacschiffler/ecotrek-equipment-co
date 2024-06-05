# Example Workflow
1. Company purchases a new wholesale product to display using POST stock/plan 

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

2. stock/deliver/{order_id}

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
“OK”
