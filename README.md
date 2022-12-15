# A Spell of Good Weather: Scraping Web Data for Temperature Insights
## Building a Web Scraping Programm for Collecting Weather Data 


1. [General Info](#General-Info)
2. [Installation](#Installation)
3. [Contributing](#Contributing)


## General Info
As part of this project, a web scraping program was developed to collect weather data - including temperature, rainfall amount, and descriptive weather information - from three selected websites. The BeautifulSoup and Request library were used for this purpose, and Regular Expressions were also used on a small scale. 
An additional essential component is the data storage in HDF5 format. For this purpose, several groups and data sets were created in the created HDF5 file, which store the scrapped information. 
Scraping was performed almost hourly over two days - the results and change in data were then read from the HDF5 and visualized in line graphs. 

The code was developed as part of a university project (B.Sc. Data Science, Data Quality and Data Wrangling). 

Key Skills I Was Able to Learn: 
* Getting familiar with BeautifulSoup and Requests for Web Scraping.
* Brief insight into Regular Expressions
* Exposure to the HDF5 file format, both creating and storing data, and reading out the information 
* In addition, in the context of a term paper, discussion of the legal and ethical aspects of web scraping as well as the general process of such a project. 


![Verlauf_Temperatur](https://user-images.githubusercontent.com/71875232/207880998-88fc118e-bf2a-40d5-a7a9-0c0aca408ff0.png)



## Installation

**Requirements:** 
Make sure you have Python 3.7+ installed on your computer.  

**Req. Package:**
* h5py
* numpy
* os (if working with cron) 
* logging 
* requests
* beautiful soup
* re
* numpy
* datetime
* pandas
* plotly.express


## Contributing 
Your comments, suggestions, and contributions are welcome. 
Please feel free to contribute pull requests or create issues for bugs and feature requests.
