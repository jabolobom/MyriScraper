from requests.exceptions import ChunkedEncodingError, ConnectionError
import env, os, requests, threading
from tqdm.tk import tqdm

class MyriDownloader:
    def __init__(self, download_path: str, url_dictionary: dict):
        self.download_path = download_path or env.DEFAULT_DOWNLOAD_PATH
        self.url_dictionary = url_dictionary

    def check_download_folder(self):
        if os.path.isdir(self.download_path):
            print(f"Downloads folder exists. Continuing...")
        else:
            os.mkdir(self.download_path)
            print(f"Downloads directory not found, directory created")

        return self.download_path
    
    def title_downloader(self, title, retries=5):
        url = self.url_dictionary[title]
        fullpath = os.path.join(self.download_path, title)
        attempt = 0

        while attempt < retries:
            try:
                with requests.get(url, stream=True) as file: # streams the file in chunks
                    file.raise_for_status() # from docs "[...] Raises HTTPError, if one occurred."

                    filesize = int(file.headers.get("content-length", 0)) or None  # from the url, gets the total file size
                    
                    with open( fullpath, "wb" ) as f, tqdm(total=filesize, leave=False, unit="B", unit_scale=True, desc=("Downloading" + title )) as bar:

                        for chunk in file.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                bar.update(len(chunk))
                
                return 
            except (ChunkedEncodingError, ConnectionError, ConnectionResetError) as e:
                attempt += 1
                print(f"Download error: {e}, retrying ({attempt}/{retries})...")

    def download_request(self, selected):
        threads = {}

        if type(selected) != list: # TODO: another callback usage
            print("ERROR: NOT A LIST! BREAKING PROCESS")
            return
        
        for i in selected:
            threads[i] = threading.Thread(target=self.title_downloader, args=(i.upper(),))
            print(f"NEW THREAD FILE: {i}")
        for i in selected:
            threads[i].start()
            print(f"DOWNLOAD STARTED FILE: {i}")
        for i in selected:
            threads[i].join()
