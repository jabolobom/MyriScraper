from myridownloader import MyriDownloader
from myriscraper import MyriScraper
from tkinter import *
from tkinter import ttk

# UI CODE HERE + summon myriscraper
def main():
    # ROOT TK
    root = Tk()
    root.title("Myriscraper Test")
    for i in range(5):
        root.columnconfigure(i, weight=1)
    for i in range(5):
        root.rowconfigure(i, weight=1)

    # MAIN FRAME
    mainframe = ttk.Frame(root, padding=10)
    mainframe.grid(row=0, column=0, sticky="nsew", rowspan=5, columnspan=5)
    for i in range(5):
        mainframe.columnconfigure(i, weight=1)
    for i in range(5):
        mainframe.rowconfigure(i, weight=0) 

    # radio buttons (SRC SELECT)
    selectedsrc = StringVar(value=None)
    
    ttk.Label(mainframe, text="Select a source: ", anchor="n").grid(row=0, column=0, sticky="nsew")
    ttk.Radiobutton(mainframe, text="Nintendo 64", value="N64", variable=selectedsrc).grid(row=1, column=0, sticky="nsew") 
    # what matters in here for us is the "value" attribute,
    ttk.Radiobutton(mainframe, text="Gamecube", value="GC", variable=selectedsrc).grid(row=2, column=0, sticky="nsew")
    ttk.Radiobutton(mainframe, text="Playstation 1", value="PSX", variable=selectedsrc).grid(row=3, column=0, sticky="nsew")
    ttk.Radiobutton(mainframe, text="Playstation 2", value="PS2", variable=selectedsrc).grid(row=4, column=0, sticky="nsew")

    # SEPARATOR BETWEEN PARTS
    ttk.Separator(mainframe, orient="vertical").grid(row=0, column=1, rowspan=5, sticky="ns", padx=10)

    # SEARCH BAR
    searchinput = StringVar()
    ttk.Label(mainframe, text="Search for a file: ", anchor="n").grid(row=2, column=3, sticky="nsew", columnspan=2)
    ttk.Entry(mainframe, textvariable=searchinput).grid(row=3, column=2, columnspan=3, sticky="nsew")

    # RESULTS FRAME
    resultsframe = Frame(mainframe, bg="white", highlightbackground="black", highlightthickness=1)
    resultsframe.grid(row=0, column=3, sticky="nsew", padx=(10,0))
    for i in range(3):
        resultsframe.columnconfigure(i, weight=1)
    for i in range(3):
        resultsframe.rowconfigure(i, weight=1)

    # TEXT RESULT
    listbox = Listbox(resultsframe, selectmode="multiple")
    scroll = Scrollbar(resultsframe, command=listbox.yview)
    listbox.configure(yscrollcommand=scroll.set)

    listbox.grid(row=0, column=0, columnspan=5, sticky="nsew")
    scroll.grid(row=0, column=6, sticky="ns")

    listbox.insert("end", "file1.zip")
    listbox.insert("end", "file2.zip")
    
    root.mainloop()

if __name__ == "__main__":
    main()