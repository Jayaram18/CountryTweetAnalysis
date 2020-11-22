import sys,tweepy,csv
from textblob import TextBlob
import json
import preprocessor as p
import PieChart
import config
class my_dictionary(dict):  
  
    # __init__ function  
    def __init__(self):  
        self = dict()  
          
    # Function to add key:value  
    def add(self, key, value):  
        self[key] = value 

class TweetSentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self):
        # authenticating your  API access
        consumerKey = config.consumerKey
        consumerSecret = config.consumerSecret
        accessToken = config.accessToken
        accessTokenSecret = config.accessTokenSecret
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)
        tweets = api.trends_available()

        # input country to find trends
        dict_obj = my_dictionary() 
        for tweet in tweets:
            dict_obj.key = tweet['name']
            dict_obj.value = tweet['woeid']
            dict_obj.add(dict_obj.key, dict_obj.value)
    
        # enter the country name available in woeid
        country = input("Enter the country name to get the latest trend:")

        # getting woeid for the country name
        country_code = dict_obj[country]
        #getting country trends for the above specified country
        country_trends = api.trends_place(country_code)
 
        trends = json.loads(json.dumps(country_trends, indent=1))
 
        trend_out = []

        for trend in trends[0]["trends"]:
            trend_out.append(trend['name'])
            print(trend["name"])




        searchTerm = input("Enter the tweet from the above list: ")
        

        # searching for trending tweets in the country
        
        if searchTerm in trend_out: 

            # Enter number of tweets to perform sentiment analysis
            NoOfTerms = int(input("Enter the number of tweets to analyze: "))
            self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)
            # Appending the tweet to csv file
            csvFile = open('clean_tweet.csv', 'a')

            # Using csv writer
            csvWriter = csv.writer(csvFile)


            # initialize the variables to analyze tweets
            polarity = 0
            positive = 0
            w_positive = 0
            s_positive = 0
            negative = 0
            w_negative = 0
            s_negative = 0
            neutral = 0


            # iterating through tweets fetched
            for tweet in self.tweets:
                #Append to temp file so that we can store in csv later.
                self.tweetText.append(p.clean(tweet.text).encode('utf-8'))
                # analysis using TextBlob
                analysis = TextBlob(tweet.text)
                # adding up polarities to find the average 
                polarity += analysis.sentiment.polarity  
                # performing normalization
                if (analysis.sentiment.polarity == 0):  
                    neutral += 1
                elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                    w_positive += 1
                elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                    positive += 1
                elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                    s_positive += 1
                elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                    w_negative += 1
                elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                    negative += 1
                elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                    s_negative += 1


            # Write to clean_tweet.csv and close csv file
            csvWriter.writerow(self.tweetText)
            csvFile.close()

            # finding the average reaction of people
            positive = self.percentage(positive, NoOfTerms)
            w_positive = self.percentage(w_positive, NoOfTerms)
            s_positive = self.percentage(s_positive, NoOfTerms)
            negative = self.percentage(negative, NoOfTerms)
            w_negative = self.percentage(w_negative, NoOfTerms)
            s_negative = self.percentage(s_negative, NoOfTerms)
            neutral = self.percentage(neutral, NoOfTerms)

            # finding average reaction
            polarity = polarity / NoOfTerms

            PieChart.plotPieChart(positive, w_positive, s_positive, negative, w_negative, s_negative, neutral, searchTerm, NoOfTerms)

        else:
            print("The search term you entered is not in the above list")


    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')



if __name__== "__main__":
    tsa = TweetSentimentAnalysis()
    tsa.DownloadData()