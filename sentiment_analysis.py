import string
import nltk
import pandas as pd
import re
import numpy as np
import psycopg2
import credentials
from nltk.corpus import stopwords
from datetime import datetime, timedelta, timezone
from sklearn import svm, tree
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import MinMaxScaler
import sys
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix

def make_dataframe_main_text(filename):
	df = pd.read_csv(filename, header = None)
	df.columns = ['time','username','subreddit','text','ticker']
	return df

def convert_date(unix_time):
    date = datetime.utcfromtimestamp(unix_time)
    return date

def categorize_subreddit(name):
    if name == 'wallstreetbets':
        return 1
    if name == 'stocks':
        return 2
    if name == 'StockMarket':
        return 3
    if name == 'Daytrading':
        return 4
    else:
        return 0

    subreddit = ['wallstreetbets', 'stocks','StockMarket','Daytrading']

def normalize(df):
    norm = df.copy()
    for cols in norm.columns:
        max_value = np.max(norm[cols])
        min_value = np.min(norm[cols])
        if  max_value != min_value:
            norm[cols] = (norm[cols] - min_value) / (max_value - min_value)
        else: 
            norm[cols] = 0
    return norm

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
    positive = set(("call",'moon','hold','buy','bull','long'))
    negative = set(('sell','put','bear','short','tank'))
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
    final['sentiment'] = None
    for i in df.index:
        count_pos = 0
        count_neg = 0
        for j in df.at[i,'text']:
            if j in pos_list:
                count_pos +=1
            if j in neg_list:
                count_neg +=1
        if count_neg > count_pos:
            final.at[i,'sentiment'] =-1
        elif count_neg < count_pos:
            final.at[i,'sentiment'] = 1
        else:
            final.at[i,'sentiment'] = 0
#         final.at[i,'value_pos'] = count_pos
#         final.at[i,'value_neg'] = count_neg
    return final


def return_stock_data(pgconnection, ticker):
    cursor = pgconnection.cursor()
    column_names = ['time','open_now','high_now','low_now','close_now','volume_now' ]
    command = 'select time, open, high, low, close, volume from stock_info where stock = \''+ ticker +'\';'                       
    try:
        cursor.execute(command)
    except Exception as e:
        print(e)
    output = cursor.fetchall()
    cursor.close()
    print('total rows in stock data: ', len(output))
    df = pd.DataFrame(output, columns=column_names)
    df = df.set_index('time')
    return df

def return_price(pgconnection, ticker,date):
    cursor = pgconnection.cursor()
    command = 'select open, high, low, close, volume from stock_info where time = \'' + str(date)+'\' and stock = \''+ ticker +'\';'                       
    try:
        cursor.execute(command)
    except Exception as e:
        print(e)
    output = cursor.fetchone()
    cursor.close()
    return output

def trading_hours(time):
    while time.hour<9:
        time = time +timedelta(hours = 1)
        while time.minute <30:
            time = time +timedelta(minutes = 1)
    if time.hour>15:
        time = time + timedelta(days = 1)
        time = time.replace(hour = 9)
        time = time.replace(minute = 30)
        time = time.replace(second = 0)
    return time


def generate_prediction_db(pgconnection, ticker, minute, hour, day):
# ticker = 'TSLA'
# minute = 0
# hour = 0
# day = 7
    cursor = pgconnection.cursor()
    statement = 'select min(time) from stock_info where stock = \''+ ticker + '\';'

    cursor.execute(statement)
    minimum_time = cursor.fetchone()
    statement = 'select max(time) from stock_info where stock = \''+ ticker + '\';'
    cursor.execute(statement)
    maximum_time = cursor.fetchone()

    # minimum_time = [datetime(2021,2,1,9,30)]
    # maximum_time = [datetime(2021,2,15,15,59)]
    time = minimum_time[0]
    time = time + timedelta(days =day, minutes = minute, hours = hour)
    time_array = []
    if time > maximum_time[0]:
        print('not enough data points')
    else:
        time = trading_hours(time)
        time_array.append(time)
        while time < maximum_time[0]:
            time = time + timedelta(minutes = 1)
            time = trading_hours(time)
            time_array.append(time)

    print('total rows in prediction table: ', len(time_array))
    pred_df = pd.DataFrame(columns=['time','average_sentiment','current_price'])
    pred_df['time'] = time_array
    return pred_df


def update_preditiction_db(pred_df, stock_price_db, minute, hour, day):
# 'open_last_time_period','high_last_time_period','low_last_time_period','close_last_time_period','volume_last_time_period'

    for i in pred_df.index:
        present = pred_df.at[i,'time']
        past = present - timedelta(days =day, minutes = minute, hours = hour)
        try:
            pred_df.at[i,'open_last_time_period'] = stock_price_db.loc[past]['open_now']
            pred_df.at[i,'high_last_time_period'] = stock_price_db.loc[past]['high_now']
            pred_df.at[i,'low_last_time_period'] = stock_price_db.loc[past]['low_now']
            pred_df.at[i,'close_last_time_period'] = stock_price_db.loc[past]['close_now']
            pred_df.at[i,'volume_last_time_period'] = stock_price_db.loc[past]['volume_now']
        except:
            pred_df.at[i,'open_last_time_period'] = np.NaN

            
def update_y_label(pred_df,stock_price_db, minute, hour, day):
    minute = 0
    hour = 1
    day = 0
    for i in pred_df.index:
        present = pred_df.at[i,'time']
        future = present + timedelta(days =day, minutes = minute, hours = hour)
        trading_hrs_check = trading_hours(future)
        if future != trading_hrs_check: 
            pred_df.at[i,'current_price'] = np.NaN
            continue
        try:
            future_price = stock_price_db.loc[future]['close_now']
            present_price = stock_price_db.loc[present]['close_now']
            percentage_diff = (future_price - present_price)/present_price
            if percentage_diff > 0:
                pred_df.at[i,'current_price'] = 1
            else:
                pred_df.at[i,'current_price'] = 0    
        except:
            pred_df.at[i,'current_price'] = np.NaN
            
def update_avg_sentiment(pred_df, sent_db, minute, hour, day):
    sent_db.dropna(axis = 0, inplace = True)
    sentiment_db = sent_db.set_index('time')
    for row in pred_df.index:
        present = pred_df.at[row,'time']
        past = present - timedelta(days =day, minutes = minute, hours = hour)
        freq_of_text = 0
        avg_sentiment = 0
        for i in sentiment_db.index:
            text_time = i #sentiment_db.at[i,'time']
            if text_time <= present and text_time >= past:
                avg_sentiment = avg_sentiment + sentiment_db.loc[i]['sentiment']
                freq_of_text += 1
        try:
            avg_sentiment = avg_sentiment/freq_of_text
            pred_df.at[row,'average_sentiment'] = round(avg_sentiment,7)
            pred_df.at[row,'frequency'] = freq_of_text
        except:
            pred_df.at[row,'average_sentiment'] = np.NaN
            pred_df.at[row,'frequency'] = np.NaN


def run_model(pgconnection ,final_df, ticker, minute, hour, day):

    # ticker = 'TSLA'
    # minute = 0
    # hour = 2
    # day = 0
    
    #print('connection set up', datetime.now())
    pred_df = generate_prediction_db(pgconnection, ticker, minute, hour, day)
    
    #print('made pred_df', datetime.now())

    tsla = return_stock_data(pgconnection, ticker)


    pred_df = pred_df.merge(tsla, how = 'left',on = 'time')
    #print('merge complete', datetime.now())
    #print(pred_df.head())
    update_preditiction_db(pred_df,tsla, minute, hour, day)
    #print('update pred_df complete', datetime.now())
    #print(pred_df.head())
    update_y_label(pred_df, tsla, minute, hour, day)
    #print('y lable created', datetime.now())
    update_avg_sentiment(pred_df, final_df, minute, hour, day)
    #print('average sentiment calculated', datetime.now())
    #pred_df.drop(['average_sentiment'], axis =1, inplace=True)
    sample = pred_df.dropna(axis = 0)
    #sample.drop(['average_sentiment','frequency'], axis =1, inplace=True)
    #sample.head()
    #print('length of table: ',len(sample))
    y = sample['current_price'].astype('int')
    sample.drop(columns = ['current_price','time'], inplace = True)
    #sample['time'] = sample['time'].apply(lambda x: x.replace(tzinfo=timezone.utc).timestamp())
    #print(y.value_counts())
    #print(len(y))
    #print("##"*30)
    #print(sample.info())
    #sample = sample.applymap(float)
    #print('ok floated')
    #print(sample.info())
    # print(sample.head())
    #print(sample['frequency'].value_counts())
    #print(sample.head())
    scaler = MinMaxScaler()
    sample = pd.DataFrame(scaler.fit_transform(sample))
    #print('###'*20)
    sample.dropna(inplace=True)
    #sample.drop(['time'], axis =1, inplace=True)
    #print(sample.head())
    print('time delay: ',minute,' minutes,',hour,' hours,',day,'days')
    x_train, x_test, y_train, y_test = train_test_split(sample, y)
    model = tree.DecisionTreeClassifier()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    #print(y_pred)
    print('Results of Decision Tree')
    print('Confusion Matrix: ')
    print(confusion_matrix(y_test, y_pred))
    print('Precision Score: ', precision_score(y_test, y_pred))
    print('Recall Score: ', recall_score(y_test, y_pred))
    print('F1 Score: ', f1_score(y_test, y_pred))
    #model1 = svm.LinearSVC()
    #model1.fit(x_train, y_train)
    #y_pred = model1.predict(x_test)
    #print('Results of Linear SVC')
    #print('Confusion Matrix: ', confusion_matrix(y_test, y_pred))
    #print('Precision Score: ', precision_score(y_test, y_pred))
    #print('Recall Score: ', recall_score(y_test, y_pred))
    #print('F1 Score: ', f1_score(y_test, y_pred))
    model2 = svm.SVC()
    model2.fit(x_train, y_train)
    y_pred = model2.predict(x_test)
    #print(y_pred)
    print('Results of SVC')
    print('Confusion Matrix: ')
    print(confusion_matrix(y_test, y_pred))
    print('Precision Score: ', precision_score(y_test, y_pred))
    print('Recall Score: ', recall_score(y_test, y_pred))
    print('F1 Score: ', f1_score(y_test, y_pred))
  
    # model.fit(x_train, y_train)
    #print('time delay: ',minute,' minutes,',hour,' hours,',day,'days')
    #print('Results of Decision Tree for ',ticker, ': ', cross_val_score(model, sample,y, cv = 3).mean())
    #print('Results of Linear SVC for ',ticker, ': ', cross_val_score(model1, sample,y, cv = 3).mean())
    #print('Results of SVC  for ',ticker, ': ', cross_val_score(model2, sample,y, cv = 3).mean())
    print('everything completed at: ', datetime.now())
    print('###'*20)



if __name__ == '__main__':


    # input filename that stores all the data obtained from API calls
    # change the file name to reddit_data_commentscsv if you want to analyze the text data from comments
    api_data = make_dataframe_main_text("reddit_data_title.csv")

    #print('----------- initial table -----------', datetime.now())
    #print(api_data.head())
    # Process the text component of the data so it is ready for sentiment analysis (look above to see what the clean_main_text function does)
    api_data['text'] = api_data['text'].apply(lambda x: clean_main_text(x))
    #convert date
    api_data['time'] = api_data['time'].apply(lambda x: convert_date(x))
    api_data['subreddit'] = api_data['subreddit'].apply(lambda x: categorize_subreddit(x))
    
    # process the Bag of positive and negative words.
    # data obtained from http://mpqa.cs.pitt.edu/
    bag_of_word_text = make_dataframe_bow("subjclueslen1-HLTEMNLP05.tff")

    # create a dataframe to work with the data easily
    BOW_df = pd.DataFrame(bag_of_word_text, columns=['type','len','word','pos','stemmed','sentiment','x']) 
    # extra column was created somehow. Just remove it
    BOW_df.drop(['x'], axis = 1, inplace=True)
    
    #print(datetime.now())
    # Now extract list of positive and negative words in 2 list
    positive, negative = give_positive_negative_word_list(BOW_df)

    #finally, use basic method to predict sentiment of every post
    final_df = gen_sentiment(api_data, positive, negative)

    # look at the tables side by side
    #print("---"*50)
    #print('sentiment table', datetime.now())
    #print(final_df.head())
    #print("---"*50)
    #print('count of positive/ negative/ neutral', datetime.now())
    #print(final_df['sentiment'].value_counts())
    final_df.drop(['username','text'], axis =1, inplace=True)
    # final_df['time'] = final_df['time'].apply(lambda x: convert_date(x))

    pgconnection = psycopg2.connect(host = credentials.SQL_HOST, dbname = credentials.SQL_DB, user = credentials.SQL_USERNAME, password = credentials.SQL_PASSWORD)
    
    for i in (1,2,4):
       run_model(pgconnection, final_df, 'TSLA',0,i,0)
#	run_model(pgconnection, final_df, 'TSLA',0,0,i)

