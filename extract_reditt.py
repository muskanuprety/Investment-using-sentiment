import praw
import datetime

reditt = praw.Reddit("bot1", user_agent = "sentiment-project-by-muskan")
wsb = reditt.subreddit("wallstreetbets")

start_date = int(datetime.datetime(2020,1,1).timestamp())


posts = wsb.top("all")
for i in posts:
	if not i.stickied and i.created_utc > start_date:

		words_in_title = i.title.split()

		keywords = ['tsla','$tsla', 'elon musk','electric vehicle','ev','elon']

		for word in words_in_title:
			if word.lower() in keywords:
				print("--"*50)
				print(i.created_utc, i.author, i.title)








# 		allc = []
# 		comm = i.comments.list()
# 		for j in comm:
# 			print(50*'--')
# 			print (j.body)

# 		print("time: {} Author: {}, title: {}, comm: {}".format(i.created_utc, i.author, i.title))
# # print(reditt.auth.scopes())