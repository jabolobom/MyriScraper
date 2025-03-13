from flask import render_template
from flask import Flask, request
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from fuzzywuzzy import process
import threading

url_dictionary = dict()
result_list = list()
PSX_url = "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/"
threads = {}

try:
    response = requests.get(PSX_url) # TEMPORARY, CHANGE THIS!!!!!!!!!!!1
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a') # get all links (not ideal, but works for every page in myrient)
except Exception as e:
    print(e)

for element in links:
    if 'title' in element.attrs and 'href' in element.attrs: # "title" is the attr used in the html page
        truelink = urljoin(PSX_url, element['href'])
        gameTitle = element['title'].upper().strip()

        url_dictionary[gameTitle] = truelink # title : download-link

print("dictionary created")

def title_search(user_search: str):
    result_list.clear()
    substring_results = [title for title in url_dictionary.keys() if user_search.upper() in title]
    if substring_results:
        for name in substring_results: # for each matching title
            result_list.append((name, url_dictionary[name])) # append (title, urldict value) tuple

        return result_list
    elif not substring_results:
        fuzzy_results = process.extract(user_search.upper(), url_dictionary.keys(), limit=100)
        filter_results = [(key, value) for key, value in fuzzy_results if value >= 80]
        return filter_results # list of tuples
    else:
        print("No results found") # PLACEHOLDER !!!!!!!!!!!!!!!!!!!
        return

def title_downloader(title, save_path):
    download = requests.get(url_dictionary[title])
    with open(save_path, 'wb') as file:
        file.write(download.content)

def download_request(selected, save_path):
    for i in selected:
        threads[i] = threading.Thread(target=title_downloader, args=(i, save_path))
    for i in selected:
        threads[i].start()
        for i in selected:
            threads[i].join()
        print("finished")