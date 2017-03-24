import requests
import json
import tweepy # need to pip install tweepy
import twitter_info # still need this in the same directory, filled out

# Fill these in in the twitter_info.py file
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


# start out cache
CACHE_FNAME = "cached_data_socialmedia.json"
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

# Then you've got to do stuff in the function!
def get_tweets_from_user(username):
	unique_identifier = "twitter_{}".format(username) # seestring formatting chapter
	# see if that username+twitter is in the cache diction!
	if unique_identifier in CACHE_DICTION: # if it is...
		print('using cached data for', username)
		twitter_results = CACHE_DICTION[unique_identifier] # grab the data from the cache!
	else:
		print('getting data from internet for', username)
		twitter_results = api.user_timeline(username) # get it from the internet
		# but also, save in the dictionary to cache it!
		CACHE_DICTION[unique_identifier] = twitter_results # add it to the dictionary -- new key-val pair
		# and then write the whole cache dictionary, now with new info added, to the file, so it'll be there even after your program closes!
		f = open(CACHE_FNAME,'w') # open the cache file for writing
		f.write(json.dumps(CACHE_DICTION)) # make the whole dictionary holding data and unique identifiers into a json-formatted string, and write that wholllle string to a file so you'll have it next time!
		f.close()

	# now no matter what, you have what you need in the twitter_results variable still, go back to what we were doing!
	tweet_texts = [] # collect 'em all!
	for tweet in twitter_results:
		tweet_texts.append(tweet["text"])
	return tweet_texts[:3]


# Let's take a look at the output in a nice way...

three_tweets = get_tweets_from_user("umich") # try with your own username, too! or other umich usernames!
for t in three_tweets:
	print("TWEET TEXT:", t)
	print("\n")