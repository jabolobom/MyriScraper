import requests
import eel
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from fuzzywuzzy import process

eel.init('../web')
eel.start('home.html', mode="firefox")

url_dictionary = dict()
url = "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/"
response = requests.get(url)
user_search = input("game name: ")

soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a')

for element in links:
    if 'title' in element.attrs and 'href' in element.attrs:
        truelink = urljoin(url, element['href'])
        gameTitle = element['title'].upper().strip()

        url_dictionary[gameTitle] = truelink

substring_results = [title for title in url_dictionary.keys() if user_search.upper() in title]
if substring_results:
    for name in substring_results:
        print(f"{name}, {url_dictionary[name]}")
else:
    fuzzy_results = process.extract(user_search.upper(), url_dictionary.keys(), limit=100)
    filter_results = [(key, value) for key, value in fuzzy_results if value >= 80]

