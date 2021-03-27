# process so far

# you can use create-database.py to create a table. But the code in extract_stock_info.py takes care of creating a table if it doesn't exist.
python extract_stock_info.py # for now it will download data for TSLA, MRNA, GME, PFE, AAPL, PTON. You can change the tickers in the main() of the python file



# although this file does make a table, for some reason, it does not create the table with the datatypes we want.
# After you run the file and load the appropriate info about the stock tickers you want, run the sql file so the columns have appropriate datatypes.
# input the appropriate parameters: h = host; d = database name; U = username; f = file name = change_datatype.sql
psql -h -d -U -f change_datatype.sql 



# next step is to pull text data. Reddit API calls are working for now.
# This file currently pulls texts filtered to only include TSLA data after 2020-01-01
# Also it looks through the following subreddits: wallstreetbets, stocks, StockMarket, Daytrading
# the keywords, dates, and subreddits to search for can be updated in the main() of this file
# You can change the keywords or change ticker symbols based on your interests
# After you make the necessary changes in the main() method of the .py file, run the file:

python extract_reddit.py #the given code only extracts posts but you can also extract comments. You will have to process the comments differently as posts are one line in csv while comments could be multi line


# You can also choose to extract data from Twitter. But I did not have access to their premium API so I could only access the latest 7 days worth of data.
# If you want twitter tweets, uncomment the next line:

#python extract_twitter.py


# Next step is to run the sentiment_analysis.py file.
# This file cleans and pre-processes the text data obtained from Reddit API calls
# This file also creates two list of positive and negative bag of words by processing file obtained from http://mpqa.cs.pitt.edu/
# you can un-comment the next line or run the command as explained in README
#python sentiment_analysis.py
