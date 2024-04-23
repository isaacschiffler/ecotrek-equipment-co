# Example Flows

## 1. Customer Purchase Example Flow
Alice has just discovered a hole in her backpack. She has a backpacking trip coming up so she needs to get a new one ASAP. First, Alice requests a catalog of backpacks that are offered by EcoTrek Equipment Co by calling GET /catalog/. She finds 20 different backpacks all at different prices. Being that she goes on backpacking trips often, she wants to purchase a more expensive, higher quality backpack. She then initiates a purchase of a backpack that costs $150. 
To do so she does the following:
* Call POST /carts/ to get a new cart with ID 333
* Alice then calls POST /carts/333/product/NORTH_FACE_BACKPACK_32 and passes the quantity 1.
* Lastly, to checkout, she calls POST /carts/333/checkout to place her order. The checkout charges her $150 and sends her a backpack.

Alice receives her backpack two days later at her door just in time for her trip.

## 2. User listing an item for sale
John is an avid garage-sale buyer, and in his excursions has come up on extra tents that he no longer needs. He wants to sell one of his tents to give it to someone that would use it more than himself. First, John posts the item with the corresponding criteria for the listing by calling POST /marketplace/. The data passed to POST includes relevant information about the product, including the product name, description, condition, and price. 
* Call POST /marketplace/ to get a new listing with an ID of 276
* Then, John calls POST /marketplace/276 and passes a quantity of 1. Now the listing is posted with the corresponding details.

John's listing for his Blue Tent is listed on the website as "for sale" for people to see.

## 3. Purchasing new stock to list for sale
Our shop has recently sold lots of items and needs to restock to make sure we have supply to fulfill demands. Thus we want to purchase more The North Face jackets and tents. 
* First, we call GET /plan to receive the wholesale catalog that The North Face offers. We will go through this catalog to find jackets and tents that we need to restock.
* Then, after submitting our plan, the supplier calls POST /stock/deliver/{orderID} in which we may for the order and receive our purchase plan.
