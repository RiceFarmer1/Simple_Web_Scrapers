
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

print("\n")
search = input("Search anything: ")

search = search.split()
query = ""

for item in search:
    query += item + "-"

htmldata = urlopen(f'https://unsplash.com/s/photos/{query}')

# Scrape html 

soup = BeautifulSoup(htmldata, 'html.parser')
images = soup.find_all('img')

# Get image data and decode

img_data = []

for i in range(1, 4):
    img_data.append(requests.get(images[i]['src']).content)

for i in range(3):
    with open(f"images_scraper/images/image{i+1}.jpg", 'wb') as handler:
        handler.write(img_data[i])

print("\n")
print("Check images folder!")
print("\n")