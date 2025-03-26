from flask import Flask, request, jsonify, render_template
import requests, webview, threading, sys, os
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from fuzzywuzzy import process

url_dictionary = dict()
result_list = list()
PSX_url = "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/"
sources = {'PSX': "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/", 
           'PS2': "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%202/",
           'N64': "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%2064%20%28BigEndian%29/"}

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


if os.path.isdir('downloads/'):
    print(f"Downloads folder exists. Continuing...")
else:
    os.mkdir('downloads/')
    print(f"Downloads directory not found, directory created")

download_path = 'downloads/'


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
    fullpath = os.path.join(save_path, title)

    if not download:
        print("download error")
        return

    with open(fullpath, 'wb') as file:
        file.write(download.content)


def download_request(selected, save_path): # SEMPRE REQUISITAR UMA LISTA DE FILES, MESMO SENDO 1 SÓ !!!!!!!!!!!!!!
    threads = {}

    if type(selected) != list:
        print("ERROR: NOT A LIST! BREAKING PROCESS")
        return

    for i in selected:
        threads[i] = threading.Thread(target=title_downloader, args=(i.upper(), save_path))
        print(f"NEW THREAD FILE: {i}")
    for i in selected:
        threads[i].start()
        print(f"DOWNLOAD STARTED FILE: {i}")
    for i in selected:
        threads[i].join()
        print(f"\nfinished downloading {i} to {save_path}")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/search', methods=["POST"])
def search():
    user_search = request.form.get("gametitle")

    if not user_search:
        return render_template("home.html")

    search_results = title_search(user_search)
    print(search_results)
    return render_template("home.html", results=search_results)


@app.route('/download', methods=["POST"])
def download():
    received = request.get_json()
    download_request(received, download_path)

    return jsonify({"status:": "download fuunction executed"}), 200


def start_flask():
    app.run(host="0.0.0.0", port=7777, debug=False)


if __name__ == "__main__":
    
    t = threading.Thread(target=start_flask)
    t.daemon = True
    t.start()

    window = webview.create_window("Scripted Download", "http://127.0.0.1:7777")
    webview.start(debug=True) # trava a execução do código pós isso
    sys.exit()
