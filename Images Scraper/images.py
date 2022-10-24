
from urllib.request import urlopen
from bs4 import BeautifulSoup

print("\n")
search = input("Enter a term: ")
  
htmldata = urlopen(f'https://unsplash.com/s/photos/{search}')

soup = BeautifulSoup(htmldata, 'html.parser')
images = soup.find_all('img')

print("\n")
print("-" * 10)
  
for i in range(1, 6):
    print("\n")
    print(images[i]['src'])

print("\n")