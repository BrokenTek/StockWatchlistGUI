# The Stock Watchlist (GUI Version) Written In Python

### Dependencies
<hr>

#### External Packages

* Beautiful Soup 4
* Requests
* Pickle
#### Standard Library

* CSV
* Datetime
* OS

<br>

### Usage
<hr>

> As a financial tracking tool, the Stock Watchlist interface is designed to focus on data.
I found it necessary to provide a way to query the most up to date data. The main function of
this tool is to provide a way for a user to easily record persistent data, being individual stock
financial data, that the user chooses to follow, building something of a persistent 'watch list'.
>
> This tool is meant to be one in a stack that would simply allow user chosen stock data to be stored
persistently in two formats, CSV and .dat (structured data). The addition of json will allow for even
more compatibility with tools for visualization, prediction, trend analysis, etc.
>
> The implementation does not use an API, however, opting for a direct scrape of data from the
[*Buisness Insider Website's*](https://markets.businessinsider.com) HTML, which is updated quickly on the end of the website.
>
> The stocks that are accessed for this tool are all included in the *S&P 500*.
>
> This application is simplistic in nature, which is a feature that lends itself to
the expedited usability it is intended to be a solution for.
> 
> The interface is graphical but simple with clearly labeled buttons and dynamically
updated, useful feedback. The saving and loading of user-contrived data is a simple
process. Buttons within the interface allow the user to export and import their watchlist
with a single button press.

### Useful Additions 
#### (To come in the revisitation of this application and integration with tools written be compatible.
<hr>

* Export data in JSON format.
* Visualize featured data analysis with libraries like pandas and numpy
* Clean interface and rediesgn layout. Additional data display box to seperate watchlist and stock data for a more convienient experience. 
