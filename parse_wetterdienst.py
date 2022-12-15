from requests import get
from bs4 import BeautifulSoup
import re
import numpy as np
import datetime as dt


# request content of the web page by using get() and store the server's response in the variable 'response'
# use BeautifulSoup to parse the 'response'
response = get('https://www.wetterdienst.de/Deutschlandwetter/Hamburg/Aktuell/')
html_soup = BeautifulSoup(response.text, 'html.parser')

# store content of temperature container
# split text to only store the temperature as a float
# data scraped = temperature in °C
temp_container = html_soup.find(attrs={'class': 'vorhersage_schrift2', 'id': 'temp_1'}).text.split('\n')[2]
temp_container = re.split('[:°]', temp_container)
temp_container = float(temp_container[1])
temp_container = np.array([temp_container]).astype(float)

# store content of rainfall container
# data scraped = amount of rainfall; measurement in mm
rainfall_container = html_soup.find(attrs={'class': 'vorhersage_schrift2', 'id': 'nieders_1'}).text.split('\n')[0]
rainfall_container = re.split('[ ]', rainfall_container)

if '-' in rainfall_container:
    rainfall_container[0] = 0
    rainfall_container = float(rainfall_container[0])
else:
    rainfall_container = float(rainfall_container[0])

rainfall_container = np.array([rainfall_container]) #.astype(float)


# store content of the weather description container in a string
# data scraped = weather description in text format
weather_container = html_soup.find(class_='weather_symbol')['title']

# store insert datetime
insert_datetime = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
