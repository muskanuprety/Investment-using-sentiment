from psaw import PushshiftAPI
import datetime
import csv


def output_title(api, sub_reddit_name, start_date, keywords, ticker):

	submissions = api.search_submissions(after=start_date,
                            		 subreddit=sub_reddit_name,
                            		 filter=['author', 'title', 'subreddit','comments','selftext'])
	
	with open('reddit_data.csv', 'w') as file:
		post_writer = csv.writer(file, delimiter=',')

		for each in submissions:
			words_in_title = each.title.split()
			# print(each.selftext)
			relevant = list(set(filter(lambda x: x.lower() in keywords, words_in_title)))
			if len(relevant)>0:
				row = [each.created_utc, each.author, words_in_title, ticker]
				post_writer.writerow(row)
				# print(row)




def output_comments(api, sub_reddit_name, start_date, keywords, ticker):

	comments = api.search_comments(q= keywords, )
	with open('reddit_data.csv', 'w') as file:
		post_writer = csv.writer(file, delimiter=',')

		for each in submissions:
			words_in_title = each.title.split()
			
			relevant = list(set(filter(lambda x: x.lower() in keywords, words_in_title)))
			if len(relevant)>0:
				row = [each.created_utc, each.author, each.title, ticker]
				post_writer.writerow(row)



if __name__=="__main__":
	api = PushshiftAPI()
	start_date = int(datetime.datetime(2020,1,1).timestamp())

	tesla_keywords = ['tsla','$tsla', 'elon musk','elon']

	subreddit = ['wallstreetbets', 'stocks','StockMarket','Daytrading']
	for i in subreddit:
		output_title(api,i, start_date,tesla_keywords,"TSLA")






















