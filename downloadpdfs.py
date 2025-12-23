import requests
from bs4 import BeautifulSoup
import json
import os
#Importing all the libraries required for this program

# this is the base directory which ensures fiels are saved according to script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# This inputs the JSON file we obtained from the scraping script
JSON_PATH = os.path.join(BASE_DIR, "kits_2024.json")

# Folder where PDFs will be saved
PDF_DIR = os.path.join(BASE_DIR, "assembly_pdfs")
os.makedirs(PDF_DIR, exist_ok=True)

# Loads scraped kit data
with open(JSON_PATH, "r", encoding="utf-8") as file:
    kits = json.load(file)

for kit in kits:
    sku = kit.get("sku")
    name = kit.get("name", "unknown_kit")

    if sku == "Not found":
        print(f"Skipping kit with missing SKU: {name}")
        continue

    # Reconstruct MiniSet page URL from SKU
    url = f"https://miniset.net/sets/gw-{sku}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Look for PDF links (assembly manuals)
    pdf_links = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.lower().endswith(".pdf"):
            pdf_links.append(href)

    if not pdf_links:
        print(f"No PDFs found for {name}")
        continue

    #This for loop allows us to download all the constituents of the list
    for pdf_url in pdf_links:
        if pdf_url.startswith("/"):
            pdf_url = "https://miniset.net" + pdf_url

        pdf_name = pdf_url.split("/")[-1]
        safe_name = name.replace(" ", "_").replace("/", "_")
        file_path = os.path.join(PDF_DIR, f"{safe_name}_{pdf_name}")

        pdf_response = requests.get(pdf_url)

        with open(file_path, "wb") as pdf_file:
            pdf_file.write(pdf_response.content)

        print(f"Downloaded: {file_path}")

print("PDF download process completed.")
