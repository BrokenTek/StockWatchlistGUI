'''
By: Carson Pribble
File: stock.py
Purpose: Create a data class for each stock. The input will
    be 8 items to populate instance variables upon initialization.
'''


class Stock(object):

    # initialize a class with 8 inputs to store as instance variables
    def __init__(self, data_list):
        self.name = data_list[0]
        self.latest_price = data_list[1]
        self.previous_close = data_list[2]
        self.lowest = data_list[3]
        self.highest = data_list[4]
        self.price_change = data_list[5]
        self.percent_change = data_list[6]
        self.date = data_list[7]

    # getter methods
    def getName(self):
        return self.name

    def getLatestPrice(self):
        return self.latest_price

    def getPreviousClose(self):
        return self.previous_close

    def getLowestPrice(self):
        return self.lowest

    def getHighestPrice(self):
        return self.highest

    def getChangeInPrice(self):
        return float(self.price_change)

    def getChangePercent(self):
        return self.percent_change

    def getDateScraped(self):
        return self.date

    def __str__(self):
        output = "Name: " + self.name + "\nLatest Price: " + self.latest_price \
                 + "\nPrevious Close: " + self.previous_close + "\nLowest Price: $" \
                 + self.lowest + "\nHighest Price: $" + self.highest + "\nChange in price: " \
                 + self.price_change + "\nPercent change: " + str(self.percent_change) + "\nDate: " \
                 + self.date
        return output
