# habyt_test
Kanjin Ogawa  
4/22/2024  

The main object of focus in the API pull is the sellable unit. A sellable unit has an address associated to it via the propertyId key, and other data such as fees, monthly pricing, and images via the id key. 

The physical address of the building is stored in a separate table to minimize duplicated data, but we keep the room number in the sellable units table because the SHARED or PRIVATE status of the sellable unit is tied to the room and not the address of the building. There's a chance floorplanName (and maybe a few others) are tied to the room and not the address, but the field was empty so there was no way for me to tell.

Fees, monthly prices, and images are stored in separate tables because they contain multiple entries per id.

There's a case to be made for keeping pricing data (minStay, minPrice, and maxPrice) in a separate table where we track changes instead of overwriting them, as there maybe interesting trends that can be picked up (like price change relative to time on market). The value of doing this depends on how often the fields change, so I suppose we have to do it to find out. Same can be said for for the monthly pricing data, but this can be handled in the merge process later on.

This schema should be robust to future changes such as renting to businesses, as we can just add a new tag in the sellable units table like this: SHARED, PRIVATE, BUSINESS.
