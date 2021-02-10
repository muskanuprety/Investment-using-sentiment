import csv
import tweepy
import credentials

auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET_KEY)
api = tweepy.API(auth)


with open('tweet_data.csv', 'w') as file:
	tweet_writer = csv.writer(file, delimiter=',')

	# tweet_writer.writerow(['tweet_date','username','userID','tweet','total_number_of_tweets_by_user','count_retweets','count_likes','count_user_followers','language'])
	keywords = "tesla OR TSLA OR Elon Musk OR Electric Vehicle OR Tesla OR $TSLA"
	date_since = "202001010000"
	date_to = "202101010000"
	# try:
		
	# for tweet in tweepy.Cursor(api.search, q= keywords, result_type = 'popular', lang = 'en', tweet_mode = 'extended').items():  #result_type = 'popular' can be put to only include popular tweets
	
	for tweet in tweepy.Cursor("research", api.search_full_archive, query = keywords, fromDate = date_since, toDate = date_to).items():
		if tweet.retweeted:
			continue
		else:
			row = [tweet.created_at, tweet.user.name, tweet.user.name, tweet.user.id, tweet.full_text, tweet.user.statuses_count, tweet.retweet_count, tweet.favorite_count, tweet.user.followers_count, tweet.lang]
			print(row)
			# tweet_writer.writerow(row)
		
	# except tweepy.TweepError:
	# 	print(tweepy.TweepError)
	# 	print(i)
		

	
			

	
		




    # print(tweet.user.name)
    # print(tweet.user.id)
    # print(tweet.full_text)
    # print(tweet.user.statuses_count)
    # print(tweet.retweet_count)
    # print(tweet.favorite_count)
    # print(tweet.user.followers_count)
    # print(tweet.lang)