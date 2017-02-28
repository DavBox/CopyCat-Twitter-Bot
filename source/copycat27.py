import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials
consumer_key = "4MEpxB7Cbm62RhKFqWujeWokG"
consumer_secret = "aFQz3pIIqkalwawSSTteddf3X9odfTQ37OV0U8elAfxdlVMeLK"
access_key = "2370874614-CeWwHE8xi945Vo2IWz8QzYe7PbvfCD0gjAxaBdn"
access_secret = "iWjHHSf2O5ATqoHJXBf41Ue7dMhrQrGVPWIlhgSyZuqNU"


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest,include_retweets=False)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
	
	pass


if __name__ == '__main__':
	username = "colin_gj"
	
	#pass in the username of the account you want to download
	get_all_tweets(username)
	
	#remove all retweets
	with open(username + '_tweets.csv', 'rb') as inp, open(username + '_filtered.csv', 'wb') as out:
		writer = csv.writer(out)
		for row in csv.reader(inp):
			if "RT" not in row[2]:
				writer.writerow(row)