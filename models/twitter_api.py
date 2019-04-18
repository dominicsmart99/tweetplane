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
