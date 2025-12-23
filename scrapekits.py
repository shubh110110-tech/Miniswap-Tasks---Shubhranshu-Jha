print("scrapekits.py started")

#Importing all the libraries which are required for the task to perform web scraping from the website along with saving JSON files
import requests
from bs4 import BeautifulSoup
import json
import re
import os


#This is to ensure that the JSON is saved in the same folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "kits_2024.json")

URL = "https://miniset.net/sets/gw-99120599084" #This is the website which is to be scraped

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")
#This part downloads page HTML and converts raw HTML into searchable form

name = soup.find("h1").text.strip()
#This extracts the name of the SKU from the webpage

desc_tag = soup.find("meta", {"name": "description"})
description = desc_tag["content"] if desc_tag else "N/A"
#This extracts the description and description tag using the BeautifulSoup library via parsing


text = soup.get_text(" ")
sku_match = re.search(r"\b99\d+\b", text)
sku = sku_match.group() if sku_match else "Unknown"
#This is the part to find the SKU Id


price_match = re.search(r"£\d+(\.\d{2})?", text)
price = price_match.group() if price_match else "Unknown"
#This finds out the last known price of the SKU

kits = [{
    "name": name,
    "description": description,
    "last_known_price": price,
    "sku": sku
}]
print("Contents are :", kits)

#this is the list which contains all of the required values basically dictionaries with keytags

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(kits, f, indent=4)

#This writes clean JSON which can be downloaded and extracted
print("Saved JSON to:", OUTPUT_FILE)
print("scrapekits.py finished")
