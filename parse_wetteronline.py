from requests import get
from bs4 import BeautifulSoup
import numpy as np
import datetime as dt


# request content of the web page by using get() and store the server's response
# use BeautifulSoup to parse the 'response'
response = get('https://www.wetteronline.de/wetter/hamburg')
html_soup = BeautifulSoup(response.text, 'html.parser')

# store content of temperature container
# data scraped = temperature in °C
temp_container_soup = html_soup.find_all(class_='value')

temp_container_raw = []
for temp in temp_container_soup:
    temp = temp.get_text()
    temp_container_raw.append(temp)

temp_container = temp_container_raw[0]

temp_container = np.array([temp_container]).astype(float)

# store insert datetime
insert_datetime = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
