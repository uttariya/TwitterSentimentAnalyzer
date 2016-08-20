x=[['ram is a good boi','shyam is a bad boi'],['no,no,no,no! i will kill him myself!','flask is god level shit!']]
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
with open('emot-dict.pkl', 'rb') as handle:
        emot_dict = pickle.load(handle)    
with open('abbr-dict.pkl', 'rb') as handle:
        abbr_dict = pickle.load(handle)
raw_tweets=list()
for i in x:
	for tweet in i:
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