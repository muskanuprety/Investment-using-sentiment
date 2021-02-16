# process so far
pip install psycopg2 pandas tweepy alpha_vantage csv sqlalchemy praw

# you can use create-database.py to create a table. But the code in extract_stock_info.py takes care of creating a table if it doesn't exist.

python extract_stock_info.py

# although this file does make a table, for some reason, it does not create the table with the datatypes we want.
# After you run the file and load the appropriate info about the stock tickers you want, run the sql file so the columns have appropriate datatypes.

psql -h -d -U -f change_datatype.sql


# this is needed to make sure you can use the premium search api from tweepy to pull archive tweets
pip install --upgrade git+https://github.com/tweepy/tweepy@master
