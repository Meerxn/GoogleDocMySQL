# GoogleDocWebScraper

Google Doc Webscraper that uses DOCS API to extract data out of a document and into a SQL Database that can be used for a LAMP server

## Description

This scraper will be used at work to find a certain section within a document in the entire huge document and extract table elements below the section. It consists of three methods MET and read_element and main.
MET: finds the type of elements and enters within element and calls read_element
read_element: reads the text_run of the element given and returns the text content
main: calls the two methods of the body content of file. After this it does some processing of searching for the section within the entire document using the search query variables. There are also inconsistent /n within the scraped data and hence that needs to be processed in main. 
Currently working on opitmizing the searching of the section along with processing of the text

## Getting Started

### Dependencies

* Use of Google DOCS api for Python 
* Used desktop application credentials from google cloud console (Need workspace account)

### Executing program

* python3 quickstart.py



## Authors

Fardeen Meeran @Meerxn

