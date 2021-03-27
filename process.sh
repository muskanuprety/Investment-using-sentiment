# process so far
pip install requests_html bs4 psaw psycopg2 pandas tweepy alpha_vantage csv sqlalchemy praw



# you can use create-database.py to create a table. But the code in extract_stock_info.py takes care of creating a table if it doesn't exist.
python extract_stock_info.py # for now it will download data for TSLA, MRNA, GME, PFE, AAPL, PTON. You can change the tickers in the main() of the python file



# although this file does make a table, for some reason, it does not create the table with the datatypes we want.
# After you run the file and load the appropriate info about the stock tickers you want, run the sql file so the columns have appropriate datatypes.
psql -h -d -U -f change_datatype.sql # h = host; d = database name; U = username; f = file name = change_datatype.sql



# this is needed to make sure you can use the premium search api from tweepy to pull archive tweets
pip install --upgrade git+https://github.com/tweepy/tweepy@master



# next step is to pull text data. Reddit API calls are working for now.
# This file currently pulls texts filtered to only include TSLA data after 2020-01-01
# Also it looks through subreddits: wallstreetbets, stocks, StockMarket, Daytrading
# the keywords, dates, and subreddits to search for can be updated in the main() of this file
python extract_reddit.py 



# This file is to clean and pre-process the text data obtained from Reddit API calls
# This file also creates two list of positive and negative bag of words by processing file obtained from http://mpqa.cs.pitt.edu/
# the program outputs two dataframe: one represents raw data obtained from Reddit, the other one shows the result of sentiment analysis.
python sentiment_analysis.py
