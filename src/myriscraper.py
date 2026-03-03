import requests
import env
from bs4 import BeautifulSoup
from fuzzywuzzy import process
from urllib.parse import urljoin

class MyriScraper:
    def __init__(self, files_dictionary: dict, result_list: list, sources: dict):
        self.files_dictionary = files_dictionary
        self.result_list = result_list
        self.sources = sources
        self.is_source_selected = False

    def getSource(self, tag):
        if tag == None:
            return False
        else:
            url = self.sources[tag]

        self.files_dictionary.clear() # clears anything that was there before

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

                self.files_dictionary[gameTitle] = truelink # title: download-link

        self.is_source_selected = True

        return self.files_dictionary
    
    def title_search(self, user_search: str): # TODO: check if there isnt a better way to do this, as were not using flask anymore
        self.result_list.clear()

        if not self.files_dictionary: return # early return if theres not a dict

        substring_results = [title for title in self.files_dictionary.keys() if user_search.upper() in title]

        if substring_results:
            for name in substring_results: # for x matching title
                self.result_list.append((name, self.files_dictionary[name])) # append (title, urldict value) tuple

            return self.result_list
        elif not substring_results:
            fuzzy_results = process.extract(user_search.upper(), self.files_dictionary.keys(), limit=100)
            filter_results = [(key, value) for key, value in fuzzy_results if value >= 80]
            
            self.result_list = filter_results

            return filter_results
        else:
            print("No results found") # TODO: make a callback function to show error/sucess messages
            return