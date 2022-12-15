from requests import get
from bs4 import BeautifulSoup
import re
import numpy as np
import datetime as dt


# request content of the web page by using get() and store the server's response in the variable 'response'
# use BeautifulSoup to parse the 'response'
response = get('https://luft.hamburg.de/clp/meteorologie/clp1/meteorology/tmp')
html_soup = BeautifulSoup(response.text, 'html.parser')

# store content of temperature container for each location
# split text to only store the temperature as a float
# data scraped = temperature in °C for three weather stations in Hamburg

# billbrook
temp_container_billbrook = html_soup.find(attrs={'class': 'lmn-table__cell lmn-table__cell--numeric '
                                                          'lmn-scrollableTable__cell lmn-scrollableTable__cell--100',
                                                 'data-lmn-th': 'Billbrook (Stundenwerte)'}).text
temp_container_billbrook = re.split('[ ]', temp_container_billbrook)[1]
temp_container_billbrook = float(temp_container_billbrook.replace(',', '.'))

# finkenwerder west
temp_container_finken = html_soup.find(attrs={'class': 'lmn-table__cell lmn-table__cell--numeric '
                                                       'lmn-scrollableTable__cell lmn-scrollableTable__cell--100',
                                              'data-lmn-th':'Finkenwerder West (Stundenwerte)'}).text
temp_container_finken = re.split('[ ]', temp_container_finken)[1]
temp_container_finken = float(temp_container_finken.replace(',', '.'))

# marckmannstraße
temp_container_marckm = html_soup.find(attrs={'class': 'lmn-table__cell lmn-table__cell--numeric '
                                                       'lmn-scrollableTable__cell lmn-scrollableTable__cell--100',
                                              'data-lmn-th':'Marckmannstraße (Stundenwerte)'}).text
temp_container_marckm = re.split('[ ]', temp_container_marckm)[1]
temp_container_marckm = float(temp_container_marckm.replace(',', '.'))

# store all temp variables in one array
data_luft_hamburg = np.array([temp_container_billbrook, temp_container_finken, temp_container_marckm]).astype(float)

# store insert datetime
insert_datetime = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
