from psaw import PushshiftAPI
import datetime
import csv


def output_title(api, sub_reddit_name, start_date, keywords, ticker):
	for key in keywords:
		submissions = api.search_submissions(title = key,
											after=start_date,
	                            		 	subreddit=sub_reddit_name,
	                            		 	filter=['author', 'title', 'subreddit'])
		
		with open('reddit_data_title.csv', "a") as file:
			post_writer = csv.writer(file, delimiter=',')

			for each in submissions:
				row = [each.created_utc, each.author, sub_reddit_name, each.title, ticker]
				post_writer.writerow(row)
					# print(row)




def output_comments(api, sub_reddit_name, start_date, keywords, ticker):
	
	for key in keywords:

		comments = api.search_comments( q= key,
										after=start_date,
										subreddit=sub_reddit_name,
										filter=['author', 'title', 'subreddit','body'] )
		with open('reddit_data_comments.csv', 'a') as file:
			post_writer = csv.writer(file, delimiter=',')

			for each in comments:
				# words_in_comments = each.body.split()
				# relevant = list(set(filter(lambda x: x.lower() in keywords, words_in_comments)))
				# if len(relevant)>0:
				# print(each)
				# print(words_in_comments)
				# if n >5:
				# 	break
		# break
				row = [each.created_utc, each.author, sub_reddit_name, each.body, ticker]
				post_writer.writerow(row)



if __name__=="__main__":
	api = PushshiftAPI()
	start_date = int(datetime.datetime(2020,1,1).timestamp())

	tesla_keywords = ['tsla','$tsla', 'tesla']
	moderna_keywords = ['moderna','$mrna','mrna']
	gamestop_keywords = ['gamestop','$gme','gme']
	pfizer_keywords = ['pfizer','pfzer','pfe','$pfe']
	apple_keywords = ['apple','$aapl','aapl']
	peloton_keywords = ['peloton','pton','$pton']


	subreddit = ['wallstreetbets', 'stocks','StockMarket','Daytrading']
	
	companies = {'TSLA':tesla_keywords, 
				'MRNA': moderna_keywords, 
				'GME': gamestop_keywords, 
				'PFE':pfizer_keywords, 
				'AAPL': apple_keywords, 
				'PTON': peloton_keywords}
	
	for company, keywords in companies.items():
		for i in subreddit:
			output_title(api, i, start_date, keywords, company)
			#output_comments(api, i, start_date, keywords, company)




















