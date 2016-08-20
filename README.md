# TwitterSentimentAnalyzer

A flask web app built to visually show the results of sentiment analysis using our model.We aggregate tweets from last seven days 
and analyze using our model. then we show the following information

  - percentage of positive to negative tweets
  
  - some sample positive and negative tweets
  
  - variation of positive and negative emotion in the last 10 days.we do not normalise the per-day data,because it gives us an insight
    into the volume of data per day.
      
### A sample report for search term *"FC Barcelona"*  looks like this

![sample image](https://raw.githubusercontent.com/uttariya/TwitterSentimentAnalyzer/master/sample_report.png)
