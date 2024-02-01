"""
App Name: Web Crawler Script
Original Source Code Date: 01/31/2024
Original Author: Tuan Lam
Last Updated Date: 02/01/2024
Last Updated Author: Tuan Lam
"""

# import beautiful soup from bs4 to extract data out of HTML from Amazon website
from bs4 import BeautifulSoup

# import requests to send requests from local PC to Amazon website + to send result to a .csv file
import requests, csv

# import pandas to store raw text (obtained from website) into proper data frame
import pandas as pd

# read the links inside of the robot.txt file and assign variable 'robot_text_file' to it
with open('robot.txt', 'r') as text_file:
    robot_text_file = text_file.read()

# since there are more than 1 link in the text file, split each link and assign variable 'urls'
urls = robot_text_file.split()

# identify our client when making the request and set the prefer language, then assign variable 'Headers'
Headers = ({
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'accept-language': 'en-US, en;q=0.5'
})

# start counting the URLs that will be scripted, starting from 0
scripted_urls = 0

# loop over each link to obtain product description, price, and availibility status, then save all to .csv file
for url in urls:

    # assign the GET request from the headers to the URL into variable 'webpage'
    webpage = requests.get(url, headers=Headers)

    # use beautifulsoup to parse 'webpage.content' into HTML format
    # then assign it to variable 'soup'
    soup = BeautifulSoup(webpage.content, 'html.parser')

    # from the 'soup' variable, find product description, price, and in-stock status
    # assign each attribute into a variable, retrieve just the content of the attribute
    # then strip off all of the unnecessary white spaces and periods if needed
    product_desc = soup.find("div", attrs={'id': 'productDescription'}).text.strip()
    price = soup.find("span", attrs={'class': 'a-price-whole'}).text.strip('.')
    in_stock = soup.find("div", attrs={'id': 'availability'}).text.strip()

    # write the outputs to a .csv file
    with open('result.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([product_desc, price, in_stock])

    print('Done with link: {}'.format(url))

    # increment by 1 for the scripted URL
    scripted_urls += 1

print('Total URLs Scripted: {}'.format(scripted_urls))

