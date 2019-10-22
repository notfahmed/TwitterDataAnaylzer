import tweepy, schedule, time, json
from pprint import pprint
from geopy.geocoders import Nominatim
numInc = 0
radius = 10
accessToken = "3939721633-EJIfdOWAcuWVjwFpsQp7Qs3P5NNyh3q7ihpC9ld"
accessToken_Secret = "wyQ9uA8vZ02Ni2fimTJegOSdIJTO95ttIJWWkDZUxl5cZ"
apiKey = "8VQzfyd9REr8gO2nesBRkJTru"
apiKey_Secret = "2CS4iYIdBq6SNSmTJCWUFJuhOjAkN4b68bXkOIS7nYouuh7r8n"


def authenticate():
	global accessToken, accesssToken_Secret, apiKey, apiKey_Secert
	authenticator = tweepy.OAuthHandler(apiKey, apiKey_Secret)
	API = tweepy.API(authenticator)
	return API

def compareResults(results_without_location, results_with_location):
	global radius
	i = 0
	results_no_location = {}
	results_location = {}
	tweetedIn = {'Tweeted within' : str(radius) + ' miles'}
	tweetedOut = {'Not tweeted within' : str(radius) + 'miles'}
	for tweet in results_without_location:
		tweets = {'Username' : tweet.user.screen_name, 'Tweet' : tweet.text}
		results_no_location[i] = {'Tweet' + str((i+1)) : tweets}
		i+=1
	i = 0
	for tweet in results_with_location:
		tweets = {'Username' : tweet.user.screen_name, 'Tweet' : tweet.text}
		results_location[i] = {'Tweet' + str((i+1)) : tweets}
		i+=1
	for x in results_no_location:
		for y in results_location:
			if results_no_location[x] == results_location[y]:
				results_no_location[x].update(tweetedIn)
				break
			else:
				results_no_location[x].update(tweetedOut)
	storeResults(results_no_location)
def storeResults(results):
	with open('output.json', 'w') as file:
		for x in results:
			json.dump(results[x], file)
			file.write('\n')

def search_without_location(searchQuery):
	results = authenticate().search(q=searchQuery, lang = "en", count = 10)
	return results

def search_with_location(latitude, longitude, searchQuery):
	global radius
	location = str(latitude) + "," + str(longitude) + "," + str(radius) + "mi"
	locationResults = authenticate().search(q = searchQuery, geocode = location, land = "en", count = 10)
	return locationResults

def geoLocator(latitude, longitude):
	geolocator = Nominatim(user_agent = "Twitter Searcher")
	coordinates = (str(latitude), str(longitude))
	location = geolocator.reverse(coordinates)
	locationPrecise = [x.strip() for x in location.address.split(',')]
	return locationPrecise[3];

def twitterSearcher(latitude, longitude, searchQuery):
	global numInc
	compareResults(search_without_location(searchQuery), search_with_location(latitude, longitude, searchQuery))
	numInc+=1

def scheduleIteration(latitude, longitude, searchQuery, iterations):
	global numInc
	schedule.every(2).minutes.do(twitterSearcher, latitude, longitude, searchQuery)
	while numInc < iterations:
		schedule.run_pending()
		time.sleep(1)

if __name__ == '__main__':
#	lati = input("Enter latitude: ")
#	long = input("Enter longitude: ")
	lati = 6.5244
	long = 3.3792 #lagos
	searchQuery = geoLocator(lati,long) + " Accident -filter:retweets"
#	searchQuery = "Lagos Accident -filter:retweets"
	twitterSearcher(lati, long, searchQuery)
	iterations = int(input("Enter how many times before schedule stops "))
	scheduleIteration(lati, long, searchQuery, iterations)