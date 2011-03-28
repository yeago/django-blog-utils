from datetime import datetime
import time
from django.conf import settings
from django.core.cache import cache
import twitter

def latest_tweet(request):
	tweet = cache.get('tweet')

	if tweet:
		return {"tweet": tweet}

	count = 0
	try:
		while not tweet or tweet.text[0] == '@':
			tweet = twitter.Api().GetUserTimeline( settings.TWITTER_USERNAME )[count]
			count += 1


		format = "%a %b %d %H:%M:%S +0000 %Y" 
		#tweet.date = datetime.strptime( tweet.created_at, format ) 2.5+
		tweet.date = datetime(*time.strptime(tweet.created_at,format)[0:5]) #2.4 fix
		cache.set( 'tweet', tweet, getattr(settings,'TWITTER_TIMEOUT',3600) )
	except:
		pass

	return {"tweet": tweet}
