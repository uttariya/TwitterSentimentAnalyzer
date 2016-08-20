import pickle,datetime
import re
import csv
import numpy as np
import matplotlib.pyplot as plt
import os
from nltk.tag import StanfordPOSTagger
from nltk.tag import StanfordNERTagger
def datelist(a):
	base = datetime.datetime.today()
	date_list = [base - datetime.timedelta(days=x) for x in range(a)]
	dates=[]
	for i in date_list:
		dates.append(str(i.date()))
	return dates
def hashtag_breaker(s):
    if(s[0]=='#'):
        s = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', s[1:])
    return s
def word_corrector(x):
    a=set(x)
    flag=0;
    temp=x;
    for i in a:
        r=r'('+i+'{3,})'
        temp=re.sub(r,i,temp)
        if(temp!=x):
            flag=1
    if(flag==1):
        return [temp,temp]
    else:
        return [temp]
def checker(t_ct):
    for i in range(len(t_ct)-1):
        t_ct[i+1]=t_ct[i]+t_ct[i+1]
    file  = open("tweetlist.txt",encoding="utf8")
    dataset =[x.strip('\n') for x in file.readlines()]
    with open('emot-dict.pkl', 'rb') as handle:
        emot_dict = pickle.load(handle)    
    with open('abbr-dict.pkl', 'rb') as handle:
        abbr_dict = pickle.load(handle)
    #store all tweets and their class, each as elements of a list
    tweets=[]
    testy = []
    raw_tweets = []
    #process dataset to convert to string
    for data in dataset:
        tweet = data
        #remove non ascii characters such as emojis
        tweet = tweet.encode('ascii','ignore').decode('ascii')
        raw_tweets.append(tweet)
        #remove URLs/user mentions
    #    print(tweet)
        tweet = re.sub(r'(?:\@|(?:(?:https?|ftp|file)://|www\.|ftp\.))\S+', '', str(tweet), flags=re.MULTILINE)    
        tweet_words = []
        for word in tweet.split():
            #normalize camel case hashtags
            word = hashtag_breaker(word)
            #convert emoticons to representative words
            if word in emot_dict:
                word = emot_dict[word].lower()+'emot'
            word = word.replace("&amp;"," and ")
            word = word.replace("&quot;","")
            word = word.replace("&lt;","")
            word = word.replace("&gt;","")
            #convert colloqial internet abbreviations to full forms
            if word.upper() in abbr_dict:
                word = abbr_dict[word.upper()]
            
            #remove symbols and numbers 
            word = re.sub("[^a-zA-Z'_-]+", ' ', word)       
            #remove stray symbols
            word = word.strip(" '_-")
            for subword in word.split():
                #convert deliberately misspelled words to their original form.
                #if the words are overemphasized (eg. goooooodd, booooooring) replace them with multiple times of the same word
                subword = subword.strip(" '_-")
                if subword == '':
                    continue
                subword = word_corrector(subword)            
                tweet_words.extend(subword)    
    #    print(' '.join(tweet_words))
        tweets.append(tweet_words)

    del dataset
    st = StanfordNERTagger('StanfordNLP/StanfordNER/classifiers/english.conll.4class.caseless.distsim.crf.ser.gz',
                        'StanfordNLP/StanfordNER/stanford-corenlp-3.6.0.jar')
    taggedtweetlist = st.tag_sents(tweets)
    del tweets
    NERExclusions = {'O','MISC','DATE','TIME','MONEY','PERCENT'}
    tweetlist = []
    for i in range(0,len(taggedtweetlist)):
        tweet_words = []
        #remove named entities
        for tagged in taggedtweetlist[i]:
            #if(tagged[1] in NERExclusions):
            if(tagged[1] != 'NNP'):
                word = tagged[0]              
                tweet_words.append(word)
            else:
                tweet_words.append('NOMINAL_ENTITY')
        tweetlist.append(tweet_words)
    del taggedtweetlist


    st = StanfordPOSTagger('StanfordNLP/StanfordPOS/models/english-caseless-left3words-distsim.tagger',
                           'StanfordNLP/StanfordPOS/stanford-postagger.jar')
    taggedtweetlist = st.tag_sents(tweetlist)
    testX = []
    for i in range(0,len(taggedtweetlist)):
        tweet_words = []
        #remove named entities
        for tagged in taggedtweetlist[i]:
            if(tagged[1] != 'PRP' and tagged[0]!='NOMINALENTITY'):
                word = tagged[0]              
                tweet_words.append(word.lower())
            else:
                if(tweet_words):
                    if(tweet_words[-1]!='NOMINAL_ENTITY'):
                        tweet_words.append('NOMINAL_ENTITY')
                else:
                    tweet_words.append('NOMINAL_ENTITY')
                
        testX.append(' '.join(tweet_words))
    del taggedtweetlist

    models = [('ti-logit','ti')]
    features=dict()
    neg_list=set()
    pos_list=set()
    prob_list=[]
    counter=0;
    for (clf,vec) in models:
        pos=0
        neg=0
        sum1=0
        #fig = plt.figure(models.index((clf,vec)))
        with open(vec+".pkl",'rb') as file:
            vectorizer = pickle.load(file)
        with open(clf+".pkl",'rb') as file:
            classifier = pickle.load(file)
        demofile = open("ValidationSetDemo"+clf+".txt","w")
        test_vectors = vectorizer.transform(testX)
        for i in range(len(raw_tweets)):
            demofile.write("RAW TWEET: "+raw_tweets[i]+"\n")
            demofile.write("PROCESSED TWEET: "+testX[i]+"\n")
            pred_prob = classifier.predict_proba(test_vectors[i])
            pred_prob = pred_prob[0]
            features[i]=pred_prob[0]
            if(pred_prob[0]>=0.6):
                neg=neg+1;
            elif(pred_prob[1]>=0.7):
                pos=pos+1
            if( counter<len(t_ct)):
                if i==(t_ct[counter]-1):
                    prob_list.append([pos,neg])
                    counter=counter+1
            demofile.write("PREDICTED PROBABILITIES : "+ str(pred_prob)+"\n")
        sum1=pos+neg;
        if(sum1>0):
            pos=pos/sum1*100;
            neg=neg/sum1*100;
        else:
            pos=0
            neg=0
            return [0,0,['not sufficient data'],['not suffieicent data']]
        sl=sorted(features, key=features.get)
        s_c=0
        while(len(pos_list)<=5):
            pos_list.add(raw_tweets[sl[s_c]])
            s_c=s_c+1
        s_c=-1
        while(len(neg_list)<=5):
            neg_list.add(raw_tweets[sl[s_c]])
            s_c=s_c-1
        #print("positive percentage-->"+str(pos)+"%")
        #x=open("results.html","w")
        demofile.write("percentage results: \npositive:"+str(pos)+"\nnegative:"+str(neg));
    for i in range(1,len(prob_list)):
        prob_list[-i][0]=prob_list[-i][0]-prob_list[-i-1][0]
        prob_list[-i][1]=prob_list[-i][1]-prob_list[-i-1][1]
    for i in range(len(prob_list)):
        prob_list[i][0]=prob_list[i][0]
        prob_list[i][1]=prob_list[i][1]
    poset=[]
    neget=[]
    for i in range(len(prob_list)):
        poset.append(float("{0:.2f}".format(prob_list[i][0])))
        neget.append(float("{0:.2f}".format(prob_list[i][1])))
    dates=datelist(len(t_ct))
    return [poset,neget,float("{0:.2f}".format(pos)),float("{0:.2f}".format(neg)),pos_list,neg_list,dates]

    
        

