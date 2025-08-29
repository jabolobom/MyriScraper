from flask import Flask, request, jsonify, render_template, session
from flask_wtf import FlaskForm
import requests, webview, threading, sys, os
from requests.exceptions import ChunkedEncodingError, ConnectionError
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from fuzzywuzzy import process
from forms import sourcesForm

# would be good to put those functions on another file and import it, main is getting too crowded
def getSource(url):
    if url == None:
        return False
    else:
        url = sources[url]

    url_dictionary.clear()

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')  # get all links (not ideal, but works for every page in myrient)
    except Exception as e:
        print(e)

    for element in links:
        if 'title' in element.attrs and 'href' in element.attrs:  # "title" is the attr used in the html page
            truelink = urljoin(url, element['href'])
            gameTitle = element['title'].upper().strip()

            url_dictionary[gameTitle] = truelink  # title : download-link


    print("List ready", url_dictionary)
    is_source_selected = True
    return url_dictionary

def check_download_folder():
    if os.path.isdir('downloads/'):
        print(f"Downloads folder exists. Continuing...")
    else:
        os.mkdir('downloads/')
        print(f"Downloads directory not found, directory created")

    download_path = 'downloads/'
    return download_path

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
        print("No results found")
        return
    

def title_downloader(title, save_path, retries=5, chunk_size=1024*1024*8):
    url = url_dictionary[title]
    fullpath = os.path.join(save_path, title)

    attempt = 0
    while attempt < retries:
        try:
            pos = os.path.getsize(fullpath) if os.path.exists(fullpath) else 0
            headers = {"Range": f"bytes={pos}-"} if pos else None

            with requests.get(url, stream=True, headers=headers, timeout=30) as r:
                r.raise_for_status()
                mode = "ab" if pos else "wb" # if resuming, "ab" append to existing file, else write new
                with open(fullpath, mode) as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)

            print(f"Finished {title} to {fullpath}")
            return fullpath

        except (ChunkedEncodingError, ConnectionError, ConnectionResetError) as e:
            attempt += 1
            print(f"Download error: {e}, retrying ({attempt}/{retries})...")
            time.sleep(3)

    raise Exception(f"Download failed after {retries} retries: {title}")


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

### FLASK CONFIG ###
SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

def start_flask():
    app.run(host="0.0.0.0", port=7777, debug=False)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = sourcesForm()
    selected_source = None
    if form.validate_on_submit():
        selected_source = form.source.data
        session['selected_source'] = selected_source
        if url_dictionary == getSource(selected_source):
            global is_source_selected
            is_source_selected = True

    if is_source_selected:
        show_warning = True
    else:
        show_warning = False


    return render_template("home.html", form=form, show_warning=show_warning)


@app.route('/search', methods=["POST"])
def search():
    user_search = request.form.get("gametitle")
    form= sourcesForm()
    form.source.data = session.get('selected_source')

    global is_source_selected

    if is_source_selected:
        show_warning = True
    else:
        show_warning = False

    if not user_search:
        return render_template("home.html", form=form)


    search_results = title_search(user_search)
    print(search_results)
    return render_template("home.html",form=form, results=search_results, show_warning=show_warning)


@app.route('/download', methods=["POST"])
def download():
    received = request.get_json()
    download_request(received, download_path)

    return jsonify({"status:": "download fuunction executed"}), 200

if __name__ == "__main__":
    
    t = threading.Thread(target=start_flask)
    t.daemon = True
    t.start()

    ## variables; could also be in a separate environment file ##
    download_path = check_download_folder()
    url_dictionary = dict()
    result_list = list()
    sources = {'PSX': "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/",
               'PS2': "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%202/",
               'N64': "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%2064%20%28BigEndian%29/"}
    is_source_selected = False
    getSource(None)

    window = webview.create_window("MyriScraper", "http://127.0.0.1:7777", min_size=(800, 800))
    webview.start(debug=True) # trava a execução do código pós isso // faz o que tem que fazer antes, depois só dentro do flask
    sys.exit()
