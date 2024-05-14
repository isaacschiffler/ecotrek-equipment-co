# Example Workflow
1. Company purchases a new wholesale product to display using POST stock/deliver/{order_id}

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
