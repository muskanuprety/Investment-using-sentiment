import psycopg2
import pandas
import alpha_vantage
import credentials



def set_connection(listt):
	pgconnection = psycopg2.connect(host = 'bowie.cs.earlham.edu', dbname = 'muprety17_db', user = 'muprety17', password = credentials.SQL_PASSWORD)
	cursor = pgconnection.cursor()
	cursor.execute('''
		insert into stock_info(name, open_price, high_price, low_price, close_price, volume) values (%s,%s,%s,%s,%s,%s)''', listt)
	print("done")


def insert_row(cursor, listt): # time, name, opening, high, low, close, volume

	cursor.execute('''
		insert into stock_info(name, open_price, high_price, low_price, close_price, volume) values (%s,%s,%s,%s,%s,%s)''', listt)
	print("done")



if __name__ == '__main__':
	cursor = set_connection(('abc','1','1','1','1','1'))
	# insert_row(cursor, ('abc','1','1','1','1','1'))


