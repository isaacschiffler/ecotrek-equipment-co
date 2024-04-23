# Example Flows

## 1. Customer Purchase Example Flow
Alice has just discovered a hole in her backpack. She has a backpacking trip coming up so she needs to get a new one ASAP. First, Alice requests a catalog of backpacks that are offered by EcoTrek Equipment Co by calling GET /catalog/. She finds 20 different backpacks all at different prices. Being that she goes on backpacking trips often, she wants to purchase a more expensive, higher quality backpack. She then initiates a purchase of a backpack that costs $150. 
To do so she does the following:
* Call POST /carts/ to get a new cart with ID 333
* Alice then calls POST /carts/333/product/NORTH_FACE_BACKPACK_32 and passes the quantity 1.
* Lastly, to checkout, she calls POST /carts/333/checkout to place her order. The checkout charges her $150 and sends her a backpack.

Alice receives her backpack two days later at her door just in time for her trip.

## 2. (User listing an item for sale?)

## 3. (Purchasing new stock to list for sale?)
