
'''
By: Carson Pribble
File: gui.py
Purpose: Create a GUi for the stock scraper / watchlist. 
    Has buttons and a textfield for display as well as a
    text field for feedback.
'''

from stockscraper import StockScraper
import pickle
from datetime import datetime
from tkinter import *
import tkinter.scrolledtext as st


class WatchListGUI(object):

    def __init__(self):
        ''' Initialize a WatchList GUI object and place all widgets in their positions.'''

        # Create empty watchlist and uninitialized stockscraper object
        self.watchlist = list()
        self.scraped = None

        # Create the window with title and size
        self.window = Tk()
        self.window.title("Stock WatchList")
        self.window.geometry("750x450")

        # Create and place opening label
        self.lbl_prompt = Label(self.window, text="Stock Scraper and Watchlist", font=("Helvetica", 14))
        self.lbl_prompt.place(x=10,y=10)

        # Create and place button to update stock data from the internet through the stockscraper
        self.btn1 = Button(self.window, text="Update Data From Internet", command=self.updateDataScrape)
        self.btn1.place(x=10,y=40)

        # Create and place button to download stock data from a .dat file
        self.btn2 = Button(self.window, text="Load Stock Data From File", command=self.updateDataFile)
        self.btn2.place(x=10, y=70)

        # Create and place button to view the watchlist
        self.btn3 = Button(self.window, text="View Watchlist", command=self.displayWatchlist)
        self.btn3.place(x=10,y=100)

        # Create and place button with an entry field to add stocks to the watchlist. contains prompt
        self.btn4 = Button(self.window, text="Add To Watchlist", command=self.addToWatchlist)
        self.btn4.place(x=10,y=130)
        self.wl_entry_lbl = Label(self.window, text="Stock Name:", font=("Helvetica", 8))
        self.wl_entry_lbl.place(x=115,y=133)
        self.entry_watchlist = Entry(self.window)
        self.entry_watchlist.place(x=180,y=133)

        # Create and place button to sort the watchlist by name
        self.btn5 = Button(self.window, text="Sort Watchlist By Name", command=self.sortByName)
        self.btn5.place(x=10, y=160)

        # Create and place button to sort the watchlist by latest price
        self.btn6 = Button(self.window, text="Sort Watchlist By Price Change", command=self.sortByPriceChange)
        self.btn6.place(x=10,y=190)

        # Create and place button to display the stock data entirely in the textarea
        self.btn7 = Button(self.window, text="View Stocks", command=self.viewStocks)
        self.btn7.place(x=10,y=220)

        # Create and place button to open a .csv file once created with all of the stock data
        self.btn8 = Button(self.window, text="Open CSV File", command=self.openFile)
        self.btn8.place(x=10,y=250)

        # Create and place label for the feedback textarea
        self.feedback_lbl = Label(self.window, text="Feedback", font=("Helvetica", 10))
        self.feedback_lbl.place(x=10,y=300)

        # Create and place textarea that will display feedback for the user
        self.feedback_text = st.ScrolledText(self.window, width=35, height=5, font=("Helvetica", 12))
        self.feedback_text.place(x=10,y=320)

        # Create and place textarea that will display all output for stock data and watchlist
        self.text_area = st.ScrolledText(self.window, width=50, height=25, font=("Helvetica", 10))
        self.text_area.place(x=350, y=10)

        # Run the window until exited (X in top right corner)
        self.window.mainloop()

    def updateDataScrape(self):
        '''Defines the scraped variable as a stockscraper object and returns feedback msg'''
        self.scraped = StockScraper()
        self.scraped.writeDataCSV()
        self.feedback_text.delete('1.0', END)
        self.feedback_text.insert(INSERT, "Stock Data Collected")
    
    def updateDataFile(self):
        '''Defines scraped variable with data from the .dat file and returns feedback msg 
            with datetime info'''
        try:
            inFile = open("stockObjects.dat", 'rb')
            sourceCollection = pickle.load(inFile)
            time = pickle.load(inFile)
            self.feedback_text.delete('1.0', END)
            success_msg = f"Stock data loaded {datetime.now():%H:%M %A %d %b %Y}." + \
                f"\nLast saved {time:%H:%M %A %d %b %Y}."
            self.feedback_text.insert(INSERT, success_msg)

        except:
            sourceCollection = None
            print("\nNo data loaded.\n")
        self.scraped = StockScraper(sourceCollection)
        self.scraped.writeDataCSV()

    def displayWatchlist(self):
        '''Displays the watchlist in the main textarea'''
        self.text_area.delete('1.0', END)
        #self.text_area.insert(INSERT, self.watchlist)
        for each in self.watchlist:
            self.text_area.insert(INSERT, each)
            self.text_area.insert(INSERT, "\n\n")    

    def addToWatchlist(self):
        '''Adds stock to watchlist if that stock name exists in the list of stock objects 
            and returns feedback msg'''
        if self.scraped:
            if self.entry_watchlist.get() != "":
                inputName = self.entry_watchlist.get()
                for stockObject in self.scraped.stock_objects:
                    if inputName == stockObject.getName():
                        self.watchlist.append(stockObject)
                        self.feedback_text.delete('1.0', END)
                        self.feedback_text.insert(INSERT, "Stock Added")
            else:
                self.feedback_text.delete('1.0', END)
                self.feedback_text.insert(INSERT, "Cannot Leave Field Blank")
        else:
            self.feedback_text.delete('1.0', END)
            self.feedback_text.insert(INSERT, "No stock list loaded")

    def sortByName(self):
        '''Sorts the watchlist by stock name'''
        self.watchlist.sort(key=lambda x: x.name)

    def sortByPriceChange(self):
        '''Sorts the watchlist by latest price'''
        self.watchlist.sort(key=lambda x: x.price_change)

    def viewStocks(self):
        '''Displays all stock object data strings in the main textarea'''
        try:
            self.text_area.delete('1.0', END)
            for each in self.scraped.getStockObjects():
                self.text_area.insert(INSERT, each)
                self.text_area.insert(INSERT, "\n\n")
        except AttributeError:
            self.feedback_text.delete('1.0', END)
            self.feedback_text.insert(INSERT, "No Stock Data Loaded")

    def openFile(self):
        '''Opens the .csv file if scraped object is initialized'''
        try:
            self.scraped.openCSV()
        except AttributeError:
            self.feedback_text.delete('1.0', END)
            self.feedback_text.insert(INSERT, "No Stock Data Loaded")

def main():
    '''Creates a WatchListGUI object which starts the GUI'''
    wl = WatchListGUI()

if __name__ == "__main__":
    main()