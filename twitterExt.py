import tweepy,time,re
from tweepy import OAuthHandler
import os,sys,re
from datetime import date, timedelta
def twitterext(query):
    tweet_set=set()
    rsent=""
    checker=re.compile('https://[0-9a-zA-Z\.\/]{1,}')
    checker2=re.compile('https://[0-9a-zA-Z\.\/]{1,}$')
    c_key="consumer_key"
    cs_key="consumer secret"
    a_token="access token"
    as_token="access secret"
    OAUTH_KEYS = {'consumer_key':c_key, 'consumer_secret':cs_key,'access_token_key':a_token, 'access_token_secret':as_token}
    auth = tweepy.OAuthHandler(OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])
    api = tweepy.API(auth)
    j=open("tweetlist.txt","w+",encoding='utf-8')
    i=0;
    tweets=[]
    tweet_cnt=[]
    for i in range(8):
        tweet_set.clear()
        try:
            len_old=len(tweets)
            y=tweepy.Cursor(api.search, q=query,lang='en',since = date.today() - timedelta(days=i+1),until= date.today() - timedelta(days=i)).items(300)
            for x in y:
                try:
                    if x.retweeted_status:
                        c=x.retweeted_status.text
                    else:
                        c=x.text
                    c= re.sub(r'(?:\@|(?:(?:https?|ftp|file)://|www\.|ftp\.))\S+', '', str(c), flags=re.MULTILINE)        
                    tweet_set.add(c)
                except:
                    pass
            tweets.extend(list(tweet_set))
            len_new=len(tweets)
            tweet_cnt.append(len_new-len_old)
        except:
            pass
    for i in tweets:
        i = i.replace('\n',' ')
        j.write(i+'\n')
        i = i.encode('ascii','ignore').decode('ascii')
        
    j.close()
    return tweet_cnt

    

