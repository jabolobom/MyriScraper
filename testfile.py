import requests, threading
from tkinter import ttk
from tkinter import *
from pathlib import Path
from tqdm.tk import tqdm

root = Tk()
root.title("Test progress bar")

mainframe = ttk.Frame(root, padding=(10))
mainframe.grid(column=10,row=10, sticky=(N, W, E, S))

url = "https://myrient.erista.me/files/TOSEC/Nintendo/64/Games/Conker%27s%20Bad%20Fur%20Day%20%282001%29%28Rare%29%28US%29.zip"
filename = Path(url).name

def downloadfile():
    with requests.get(url, stream=True) as file: # streams the file in chunks
        file.raise_for_status() # from docs "[...] Raises HTTPError, if one occurred."

        total = int(file.headers.get("content-length", 0)) or None # from the url, gets the total file size

        with open( filename, "wb" ) as f, tqdm( total=total, leave=False, unit="B", unit_scale=True, desc=("Downloading:" + filename) ) as bar: # writebinary

            for chunk in file.iter_content(chunk_size=8192): # why 8192? most resources say is the right way/amount, but none explain it
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))
            
def start():
    threading.Thread(target=downloadfile, daemon=True).start()


ttk.Button(mainframe, text="Download", command=start).grid()

root.mainloop()