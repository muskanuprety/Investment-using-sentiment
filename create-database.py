import psycopg2
import credentials

pgconnection = psycopg2.connect(host = 'bowie.cs.earlham.edu', dbname = 'muprety17_db', user = 'muprety17', password = credentials.SQL_PASSWORD)

print('Successful connection')

cursor = pgconnection.cursor()
cursor.execute('''
	drop table if exists stock_info;

	create table stock_info (
			index serial PRIMARY KEY,
			time timestamp,
			stock varchar(255),
			open int,
			high int,
			low int,
			close int,
			volume int
	)

	''')
print('table created')

pgconnection.commit()
pgconnection.close()