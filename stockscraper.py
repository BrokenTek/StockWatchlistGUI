'''
By: Carson Pribble
File: StockScraper.py
- Scrapes data from each of the 11 pages on the website 'https://markets.businessinsider.com/index/components/s&p_500'.

METHODS
- getDataFormatted(): returns the data in a list that contains inner lists, each inner list being a stocks data
- printData(): prints the data to the console
- writeData(): writes the data to a csv file
'''

from bs4 import BeautifulSoup as bs
import requests
import csv
from os import startfile
from stock import Stock
import pickle
from datetime import datetime


class StockScraper(object):

    # initializer for creating instance. an instance will contain all the data upon declaring an object of this type.
    def __init__(self, sourceCollection=None):
        self.url = "https://markets.businessinsider.com/index/components/s&p_500"
        self.data_lists = list()  # creates the list that will contain each inner list. data_lists length will be 5 but the inner lists will be ~490 in length
        self.stock_objects = list()
        self.scrapeData()  # automatically populate the data_lists attribute upon initialization
        if sourceCollection:
            self.stock_objects = sourceCollection
        else:
            self.createStockObjects()

    # this is a void function, just used to populate the self.data_lists attribute
    # ***** THIS METHOD IS CALLED IMPLICITLY WHEN StockScraper OBJECT IS INITIALIZED ****************
    def scrapeData(self):
        # create inner lists
        names_list = list()
        price_list = list()
        low_high_list = list()
        plusminus_percent_list = list()
        time_date_list = list()

        # creates a list of urls. each url is the main url with an 
        #   appended page number.
        url_page_list = list()
        for i in range(1, 12):
            url_page = self.url + "?p=" + str(i)
            url_page_list.append(url_page)

        for url in url_page_list:

            # get page and create parser
            page = requests.get(url)
            soup = bs(page.content, 'html.parser')

            # get the table body containing the data
            body = soup.find(class_="table__tbody")

            # get the table rows
            table_rows = body.select("tr")

            # get initial data and append to the inner lists
            for table_row in table_rows:
                table_data = table_row.select("td")
                name = table_data[0].get_text().strip()
                prices = table_data[1].get_text().strip()
                low_high = table_data[2].get_text().strip()
                plusminus_percent = table_data[3].get_text().strip()
                time_date = table_data[4].get_text().strip()

                # append to the inner lists
                names_list.append(name)
                price_list.append(prices.replace("\n", " "))
                low_high_list.append(low_high.replace("\n", " "))
                plusminus_percent_list.append(plusminus_percent.replace("\n", " "))
                time_date_list.append(time_date.replace("\n", " "))

        # append each inner list to the instance attribute (self.data_lists)
        self.data_lists.append(names_list)
        self.data_lists.append(price_list)
        self.data_lists.append(low_high_list)
        self.data_lists.append(plusminus_percent_list)
        self.data_lists.append(time_date_list)

    # creates a list of objects representing stocks instead of a list of lists representing stocks
    # ***** THIS METHOD IS CALLED IMPLICITLY WHEN A StockScraper OBJECT IS INITIALIZED ******************
    def createStockObjects(self):
        # get data from method as lists
        data = self.getDataLists()

        # create another list containing stock objects
        for item in data:
            stock = Stock(item)
            self.stock_objects.append(stock)

    def __len__(self):
        return len(self.stock_objects)

    def getStockObjects(self):
        '''gets the list of stock objects.'''
        return self.stock_objects

    # gets the data formatted into a list of lists with the full stock data in each inner list
    # this method is best for getting stock data returned as a list of lists
    def getDataLists(self):

        # creates a list of lists. each inner list will be one stocks data
        list_of_stocks = list()

        # creates individual lists containing stock data and appends those inner lists to list_of_stocks
        for i in range(len(self.data_lists[0])):
            stock = list()
            stock.append(self.data_lists[0][i])  # appends the stock name
            stock.append(self.data_lists[1][i].split()[0])  # appends latest price
            stock.append(self.data_lists[1][i].split()[1])  # appends previous close price
            stock.append(self.data_lists[2][i].split()[0])  # appends low
            stock.append(self.data_lists[2][i].split()[1])  # appends high
            stock.append(self.data_lists[3][i].split()[0])  # appends price change
            stock.append(self.data_lists[3][i].split()[1])  # appends price change percentage (can be negative)
            stock.append(self.data_lists[4][i].split()[5])  # appends date
            list_of_stocks.append(stock)  # appends the stock data, which is a list, into the outer list
        # returns the data
        return list_of_stocks

    # prints the data to the console in a formatted fashion
    def printData(self):

        for stock in self.stock_objects:
            print(stock)
            print()

        # writes the data of each stock to a .csv file (for Excel or similiar editor)

    def writeData(self):
        try:
            outFile = open("stockObjects.dat", 'wb')
            sourceCollection = list()
            for each in self.stock_objects:
                sourceCollection.append(each)
            time = datetime.now()
            pickle.dump(sourceCollection, outFile)
            pickle.dump(time, outFile)
            outFile.close()
            print(f"{len(self)} stocks saved to file {time:%H:%M %A %d %b %Y}.")
        except:
            print("Stock data not saved to file.")

    def writeDataCSV(self):
        '''writes the data of each stock to a .csv file (for Excel or similiar editor)'''
        # creates or opens and overwrites an excel file to hold data
        f = open('stock_data.csv', 'w')
        # create writer with csv library
        writer = csv.writer(f)
        # writer heading to csv file
        writer.writerow(["Name", "Latest Price", "Previous Close", "Low","High", "Change", "Percent Change", "Date"])
        # get the data in format
        data = self.getDataLists()
        # write the data for each stock on a different line
        for stock in data:
            writer.writerow(stock)
        # close the file
        f.close()

    def openCSV(self):
        try:
            startfile(".\stock_data.csv")
        except:
            print("No File Exists")