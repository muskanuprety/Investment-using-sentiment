import psycopg2
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import credentials
import csv
from sqlalchemy import create_engine



def set_connection(): # sets up the connection to POSTGRESQL database
	uri = 'postgresql+psycopg2://'+ credentials.SQL_USERNAME + ':' + credentials.SQL_PASSWORD+'@' + credentials.SQL_HOST +'/' + credentials.SQL_DB
	engine = create_engine(uri)
	return engine
	# pgconnection = psycopg2.connect(host = 'bowie.cs.earlham.edu', dbname = 'muprety17_db', user = 'muprety17', password = credentials.SQL_PASSWORD)
	# cursor = pgconnection.cursor()
	# return pgconnection, cursor


# def insert_row(connection, cursor, listt): # time, name, opening, high, low, close, volume
# 	cursor.execute('''COPY stock_info(date, name, open_price, high_price, low_price, close_price, volume) values (%s,%s,%s,%s,%s,%s,%s)''', listt)
# 	conn.commit()


# def close_connection(conn, cursor):
# 	conn.close()
# 	cursor.close()


def get_data(ticker, engine): # give a list of ticker symbols and the engine object from sqlalchemy
	ts = TimeSeries(key = credentials.VANTAGE_API, output_format='csv') 
	for company in ticker:
		for i in range(1,13):
			month = 'year1month'+str(i)
			data_csv = ts.get_intraday_extended(symbol=company,interval='1min', slice = month)
			df = pd.DataFrame(list(data_csv[0]))
			df.columns = df.iloc[0]
			df = df.drop(0)
			df['stock'] = company
			df.to_sql("stock_info", engine, if_exists='append')

	# print(list(data_csv[0]))

	# with open(data_csv,'r') as file:
	# 	reader = csv.read(file)
	# 	for i in reader:
	# 		print(i)

if __name__ == '__main__':
	# stocks so far: TSLA, MRNA, GME, PFE, AAPL, PTON
	engine = set_connection()
	get_data(['TSLA','MRNA','GME','PFE','AAPL','PTON'], engine)
	


