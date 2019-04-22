from tweepy import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream 
#from credentials import *
from tweepy import API
from tweepy import Cursor 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import re


ACCESS_TOKEN = "1118229516256776194-8F2psTgSzPoX2Yfw1T9PkHbu6jj7lr"
ACCESS_TOKEN_SECRET = "AjfGgtmBXg2EIxaQNCBSUR1QJPZVGeuMm9nxmqlthFF8l"
CONSUMER_KEY = "vrrAuvS5lcCDU8KWPJIELXNja"
CONSUMER_SECRET = "eOJ0DquGEmxfFFhaB03ygk5f67khCbZ9WH5sjdO1gT3MTbUXwe"
BLUDEVGROUP_ID = 1118229516256776194


class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET) #authentication that uses consumer credentials
        auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
        #using consumer key + secret, set access tokens
        return auth
        
        
    
class TwitterStreamer():
    '''
    class for processing live tweets
    '''
    def __init__(self):
        self.twitterAuthenticator = TwitterAuthenticator()
        
        
    def stream_tweets(self, fetched_filename,hashlist):
        #handles authentication and connection to the twitter API
        listener = TwitterListener() #creates a listener object, how do i deal with the tweets and how do i deal with the errors
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth,listener)
        stream.filter(track=hashlist) #filter method from the stream class that takes a list of key terms
    

class TwitterListener(StreamListener):
    '''
    prints received tweets to standard out
    '''
    def __init__(self, fetched_filename):
        self.fetched_filename = fetched_filename
        
    def on_data(self,data):
        try:
            print(data)
            with open(self.fetched_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: " + str(e))
    def on_error(self,status):
        if status == 420:
            #returning false on_data method in the event of a rate limit
            return False
        print(status)
        
class TweetAnalyzer():
    def tweets_to_dataframe(self,tweets):
        dF = pd.DataFrame(data = [tweet.text for tweet in tweets], columns = ['tweets']) #declarative statement where we provide the DataFrame function with a list of tweets
        dF['handle'] = np.array([tweet.user.name for tweet in tweets])
        dF['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        dF['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        #dF['len'] = np.array([len(tweet.text) for tweet in tweets])
        dF['date'] = np.array([tweet.created_at for tweet in tweets])
        #dF['source'] = np.array([tweet.source for tweet in tweets])
        return dF
        #Creating a dataframe from a list of tweets
    #analyzing content of tweets
    def append_sentiment(self,df,tweet_analyzer):
        df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
        return df
    
    def convert_df_to_dictionary(self,df):
        dic = df.to_dict('records')
        return dic
    
    def clean_tweet(self,tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    def analyze_sentiment(self,tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1
    
             
class TwitterClient():
    def __init__(self,twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client =  API(self.auth)
        self.twitter_user = twitter_user
        self.user = self.twitter_client.get_user(BLUDEVGROUP_ID)

    def get_user_timeline_tweets(self,num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
    
    def get_friend_list(self,num_friends):
        friendList = []
        for friend in Cursor(self.twitter_client.friends).items(num_friends):
            friendList.append(friend)
        return friendList
    def get_home_timeline_tweets(self,num_tweets):
        homeList = []
        for tweet in Cursor(self.twitter_client.home_timeline).items(num_tweets):
            homeList.append(tweet)
        return homeList
    
    def get_twitter_client_api(self):
        return self.twitter_client
    
    def get_tweets_by_handle(self,id_list):
        tweet_list = []
        for twit_id in id_list:
            for tweet in Cursor(self.twitter_client.user_timeline, id=twit_id).items(3):
                tweet_list.append(tweet)
        return tweet_list
    
    def get_user_to_dict(self):
       
        return {
                "username": self.user.name,
                "bio": self.user.description,
                "followers_count": self.user.followers_count
                }
  
    def post_tweets(self, post_content):
        self.twitter_client.update_status(post_content)
        
    def delete_last_tweet(self,tweet):
        for last_tweet in tweet:
            self.twitter_client.destroy_status(last_tweet.id)
    
    
    
    
def create_chart(dic):
    pos = 0
    neut = 0
    neg = 0
    for rec in dic:
        if rec['sentiment'] == 1:
            pos += 1
        elif rec['sentiment'] == 0:
            neut += 1
        else:
            neg += 1
     
    objects = ('Positive', 'Negative','Neutral')
    y_pos = np.arange(len(objects))
    senti = [pos,neg,neut]
    
    plt.bar(y_pos,senti,align='center', alpha=0.5)
    plt.xticks(y_pos,objects)
    plt.ylabel('NUMBER OF TWEETS')
    plt.title('SENTIMENT')
    
    plt.show()


    

'''
from tweepy import StreamListener, OAuthHandler, Stream
from credentials import *
class StdOutListener(StreamListener):

	def on_data(self, data):
		print(data + '\n')
		return True
	
	def on_error(self, status):
		print(str(status) + '\n')

listener = StdOutListener()
auth = OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

stream = Stream(auth, listener)

stream.filter(track=['hentai'])
'''
