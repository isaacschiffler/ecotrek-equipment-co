# User Stories and Exceptions

## User Stories
1. As an environmentalist, I want to buy used goods so that I can employ sustainable equipment purchasing practices.
2. As someone who is new to backpacking, I want to be able to rent a light tent since I do not already own one so that I do not have to purchase a tent that I might not use more than once.
3. As an avid backpacker that likes to update my equipment, I want to be able to offer my old equipment up for sale so that it doesn't collect dust in my storage.
4. As someone looking for a used sleeping bag, I want to be able to see the condition of items I'm looking at so I buy something that isn't too overused.
5. As an event organizer, I want to be able to rent multiple items in large quantities so that I can accommodate large groups during corporate outdoor events.
6. As a novice camper, I want to see items categorized by type, so I can make informed decisions based on comparing similar equipment.
7. As a cold-weather camper, I want to find and rent specially insulated gear that is suitable for extreme cold, so I can camp safely in winter conditions.
8. As the parent of four young children, I want to be able to sell out-grown equipment and have basic renting options available so that I don't have more equipment than I need at one time.
9. As someone who prefers hotels and does not enjoy rugged outdoors camping, I want to be able to purchase higher-end tents and am willing to spend more for this luxury so that my camping experience is nicer.
10. As a climber, I want to find climbing shoes that are my size and in my price range so that I can more easily find what I need.
11. As a student who doesn't have much storage space, I want to be able to rent equipment only for the time that I use it and for an affordable price so that I don't have to spend lots of money and store equipment myself.
12. As someone who is from a different state, I want to rent equipment from CA so I don't have to fly my equipment out.


## Exceptions
1. If a customer's card is declined, the cart will give an error and ask to retry a different card.
2. If a customer has an item in their cart that goes out of stock, the cart will notify them and remove it from their cart.
3. If a customer intended rent dates overlap with a previous reservation, the cart will notify them and suggest the next closest rent dates.
4. If a customer's contact information is incomplete or formatted incorrectly during checkout (ie. missing phone numbers, invalid email addresses), the cart will prompt them to input the information before the order can be finalized.
5. If a customer tries to rent an item but inputs a rental return date that is before the start date, the cart will display an error message and prompt them to enter a correct return date.
6. If a customer's rental period ends but they have not returned the item, the system will automatically charge a late fee and send a notification for return.
7. If a customer wants to return an item that's overdue, the cart will throw an error and not accept back the item.
8. If a customer wants to purchase something that is **not** for sale (ie, on hold), the cart will notify them accordingly and remove from cart.
9. If a customer tries to add an item that exceeds the max size possible of a cart, the cart will notify them and will not add that item.
10. If a customer tries to rent an item for longer than max allowed time, the cart will notify them and only enter the max amount of time.
11. If a customer wants to buy or rent more of an item than is in stock, the cart will notify them and enter the current stock.
12. If a customer tries to rent an item that has been damaged, the cart will not allow this and either notify them when it will be fixed or that it is being removed from the stock.

