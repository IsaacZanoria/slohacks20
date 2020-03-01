import requests
from bs4 import BeautifulSoup

URL = "https://www.namus.gov/MissingPersons/Case#/1"
r = requests.get(URL)

soup = BeautifulSoup(r.content)
print(soup.prettify())