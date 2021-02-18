import string
import nltk
import pandas as pd
import re
import numpy as np
from nltk.corpus import stopwords


def make_dataframe_main_text(filename):
	df = pd.read_csv(filename, header = None)
	df.columns = ['time','username','text','ticker']
	return df

def clean_main_text(text_list):
    
    # The text column looks like a list but is in string format. 
    #Remove all unnecessary symbols, lowercase everything, and make a list of words
    text_list = ''.join(i for i in text_list if i.isalpha() or i in [' ']).lower().split()

    # Remove all other punctuations.
    punct = string.punctuation
    for word in text_list:
        word = ''.join(i for i in word if i not in punct)
        
    # Remove stop words that dont add value to sentiment analysis
    stop_words = stopwords.words('english')
    stop_words = set(stop_words)
    text_list = [word for word in text_list if word not in stop_words]
    
    # Remove the words we know are in the text which adds nothing to sentiment analysis
    # We know these words are here because they were the keywords we used to filter texts
    text_list = [word for word in text_list if word not in ['tsla','elon','musk']]
    
    # stemming the words to reduce them to core words
    ps = nltk.PorterStemmer()
    text_list = [ps.stem(word) for word in text_list]
    return text_list

def fix_words_bow(list_BOW):
    for i in range(len(list_BOW)):
        list_BOW[i] = re.sub(r'^.*?=', '', list_BOW[i])
    return(list_BOW)


def make_dataframe_bow(BOW_filename):
    with open(BOW_filename,'r') as read_file:
        content = read_file.read()
        read_file.close
    list_stuff = list(re.split('\n', content))
    for i in range(len(list_stuff)):
        list_stuff[i] = list(re.split(' ', list_stuff[i]))
        list_stuff[i] = fix_words_bow(list_stuff[i])
    return list_stuff

def give_positive_negative_word_list(df):
    positive = set()
    negative = set()
    ps = nltk.PorterStemmer()
    for i in range(len(df)):
        if df.iloc[i]['stemmed'] == 'n':
            df.iloc[i]['word'] = ps.stem(df.iloc[i]['word'])
        if df.iloc[i]['sentiment'] == 'negative':
            negative.add(df.iloc[i]['word'])
        if df.iloc[i]['sentiment'] == 'positive':
            positive.add(df.iloc[i]['word'])
    return list(positive), list(negative)


def gen_sentiment(df,pos_list,neg_list):
    final = df.copy()
    final['sentiment'] = 0
    final['value_pos_neg'] = None
    for i in df.index:
        count_pos = 0
        count_neg = 0
        for j in df.at[i,'text']:
            if j in pos_list:
                count_pos +=1
            if j in neg_list:
                count_neg +=1
        if count_neg == 0 and count_pos == 0:
            final.at[i,'sentiment'] = 0
        if count_neg > count_pos:
            final.at[i,'sentiment'] =-1
        if count_neg < count_pos:
            final.at[i,'sentiment'] = 1
        final.at[i,'value_pos_neg'] = (count_pos,count_neg)
    return final



if __name__ == '__main__':
	
	# input filename that stores all the data obtained from API calls
	api_data = make_dataframe_main_text("reddit_data.csv")

	print(api_data.head())
	# Process the text component of the data so it is ready for sentiment analysis (look above to see what the clean_main_text function does)
	api_data['text'] = api_data['text'].apply(lambda x: clean_main_text(x))

	# process the Bag of positive and negative words.
	# data obtained from http://mpqa.cs.pitt.edu/
	bag_of_word_text = make_dataframe_bow("subjclueslen1-HLTEMNLP05.tff")

	# create a dataframe to work with the data easily
	BOW_df = pd.DataFrame(bag_of_word_text, columns=['type','len','word','pos','stemmed','sentiment','x']) 
	# extra column was created somehow. Just remove it
	BOW_df.drop(['x'], axis = 1, inplace=True)

	# Now extract list of positive and negative words in 2 list
	positive, negative = give_positive_negative_word_list(BOW_df)

	#finally, use basic method to predict sentiment of every post
	final_df = gen_sentiment(api_data, positive, negative)

	# look at the tables side by side
	print("---"*50)
	print(final_df.head())









