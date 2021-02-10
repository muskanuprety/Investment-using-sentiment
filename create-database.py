import psycopg2
import credentials

pgconnection = psycopg2.connect(host = 'bowie.cs.earlham.edu', dbname = 'muprety17_db', user = 'muprety17', password = credentials.SQL_PASSWORD)

print('Successful connection')

cursor = pgconnection.cursor()
cursor.execute('''
	drop table if exists stock_info;

	create table stock_info (
			index serial,
			
			name varchar(255),
			open_price int,
			high_price int,
			low_price int,
			close_price int,
			volume int
	)

	''')
print('table created')

pgconnection.commit()
pgconnection.close()