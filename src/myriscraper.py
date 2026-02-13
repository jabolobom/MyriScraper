import requests, os, threading
from bs4 import BeautifulSoup
from fuzzywuzzy import process
import env


class MyriScraper:
    def __init__(self, download_path: str, url_dictionary: dict, result_list: list, sources: dict, is_source_selected: bool):
        self.download_path = env.DEFAULT_DOWNLOAD_PATH
        self.url_dictionary = url_dictionary
        self.result_list = result_list
        self.sources = sources
        self.is_source_selected = False

    def getSource(self, url):
        if url == None:
            return False
        else:
            url = self.sources[url]

        self.url_dictionary.clear() # clears anything that was there before

        try: 
            response= requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all('a') # get all links (not ideal, but works for every page in myrient)
        except Exception as e:
            print(e)
            
        for element in links:
            if 'title' in element.attrs and 'href' in element.attrs:
                truelink = urljoin(url, element['href'])
                gameTitle = element['title'].upper().strip()

                self.url_dictionary[gameTitle] = truelink # title: download-link

        print("List ready", self.url_dictionary)
        self.is_source_selected = True

        return self.url_dictionary
    
    def check_download_folder(self):
        if os.path.isdir(self.download_path):
            print(f"Downloads folder exists. Continuing...")
        else:
            os.mkdir('downloads/')
            print(f"Downloads directory not found, directory created")

        return self.download_path
    
    def title_search(self, user_search: str): # TODO: check if there isnt a better way to do this, as were not using flask anymore
        self.result_list.clear()

        if not self.url_dictionary: return # early return if theres not a dict

        substring_results = [title for title in self.url_dictionary.keys() if user_search.upper() in title]

        if substring_results:
            for name in substring_results: # for x matching title
                self.result_list.append((name, self.url_dictionary[name])) # append (title, urldict value) tuple

            return self.result_list
        elif not substring_results:
            fuzzy_results = process.extract(user_search.upper(), self.url_dictionary.keys(), limit=100)
            filter_results = [(key, value) for key, value in fuzzy_results if value >= 80]
            
            self.result_list = filter_results

            return filter_results
        else:
            print("No results found") # TODO: make a callback function to show error/sucess messages
            return
        
    def title_downloader(self, title): #TODO: MAKE THIS
        pass 

    def download_request(self, selected):
        threads = {}

        if type(selected) != list: # TODO: another callback usage
            print("ERROR: NOT A LIST! BREAKING PROCESS")
            return
        
        for i in selected:
            threads[i] = threading.Thread(target=self.title_downloader, args=(i.upper(), self.download_path))
            print(f"NEW THREAD FILE: {i}")
        for i in selected:
            threads[i].start()
            print(f"DOWNLOAD STARTED FILE: {i}")
        for i in selected:
            threads[i].join()

