# amazon_webscraping

Beautiful soup library is used to web scrape the amazon webpages. 
The provided excel file is read by using the function read_excel from pandas library. 
Two different lists are maintained for both ansi and country codes and the values of these lists are imported from the excel sheet. 
We loop through these lists and form an amazon link for the combinations of country codes and ansi values.
For every pair of country code and ansi values we send a GET request to the corresponding amazon page and check if the response code is 404 or not. 
If 404 then we skip and move to next pair of country code and ansi value. 
Otherwise, we scrape the webpage and take product title from element having id ”productTitle”, price from element having attributes class = “a-offscreen” and we retrieve image link from the block having id = “img-canvas”. Different functions are created for performing each of these tasks. A dictionary is formed with these values and appended into a list. These values are also stored on an online hosted database, elephantSQL.
After performing the above tasks for every pair of ansi and country codes, we convert the list containing every dictionary to a json object using json.dumps and then write this json object to a json file.
For snapshot of values in database, refer to readme.pdf in the repository.
