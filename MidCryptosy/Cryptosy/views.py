from multiprocessing.sharedctypes import Value
from matplotlib.font_manager import json_load

from pkg_resources import ResolutionError
import function_api as func_api
from django.shortcuts import render
from django.http import Http404,HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import nltk
import os
import pycountry
import re
import string
from PIL import Image
from langdetect import detect
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
from datetime import datetime


# authenticating
consumerKey = 'fvdx4gYvsoTZsfJz8JHbr3prd'
consumerSecret = 'W1slcbHUxqsRc2V9rKuAucuu3mAZnaVcNNjJs50rUUD80BcLif'
accessToken = '989033523947495424-2lrvMkgcdl4BsGf47LXnUAf87QvgBPX'
accessTokenSecret = 'jdoLWezl6GbyRPwiXBAaJLSgwHEAECaQHvSbnixGZgaYt'
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)
""" nltk.download('vader_lexicon') """

""" time="" """


def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity


def getPolarity(text):
    return TextBlob(text).sentiment.polarity

# for removing mentions
def cleanTxt(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)  
    text = re.sub(r'#', '', text)
    text = re.sub(r'RT[\s]+', '', text)
    text = re.sub(r'https?:\/\/S+', '', text)
    return text


def index(request):
    return render(request, 'index.html')




def Percentage(part, whole):
    return (100*float(part)/float(whole))




def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'


@api_view(["POST"])
def SentimentAnalyzer(hd):
    try:
        data= json.loads(hd.body)  
        """ coin_name = str(h).lower() """
        temp_coin=data['h'] #naming the key as h while accepting the json data-POST method
        coin_name=str(temp_coin).lower()
        print(coin_name)
        noOfTweet = 100
        tweets = tweepy.Cursor(api.search, q=coin_name, lang='en', tweet_mode='extended').items(noOfTweet)
        
      
        tweet_list = []
        i = 1
        for tweet in tweets:
            """ print(tweet.full_text) """
            tweet_list.append(tweet.full_text)
            i = i+1
        

        df = pd.DataFrame(tweet_list, columns=['Tweets'])

       
        df['Tweets'] = df['Tweets'].apply(cleanTxt)

        
        df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)

        avgSub = df['Subjectivity'].mean()
        df['Polarity'] = df['Tweets'].apply(getPolarity)
        
        df['Analysis'] = df['Polarity'].apply(getAnalysis)

        

        j = 0
        sortedDF = df.sort_values(by=['Polarity'])
        for i in range(0, sortedDF.shape[0]):
            if(sortedDF['Analysis'][i] == 'Positive'):
                j = j + 1

        
        k = 0
        sortedDF = df.sort_values(by=['Polarity'])
        for i in range(0, sortedDF.shape[0]):
            if(sortedDF['Analysis'][i] == 'Negative'):
                k = k + 1
        
        ptweets = df[df.Analysis == 'Positive']
        
        ptweets = ptweets['Tweets']
        
        positive = round((ptweets.shape[0] / df.shape[0])*100, 1)
        
        
        negtweets = df[df.Analysis == 'Negative']
        negtweets = negtweets['Tweets']
        negative = round((negtweets.shape[0] / df.shape[0])*100, 1)
        
        neutweets = df[df.Analysis == 'Neutral']
        neutweets = neutweets['Tweets']
        neutral = round((neutweets.shape[0] / df.shape[0])*100, 1)
        return JsonResponse({"Positive":positive,"Neutral":neutral,"Negative":negative,"Subjectivity":avgSub}, safe=False)
        """ return JsonResponse("coinname:"+h,safe=False) """
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def TechnicalAnalysis(coinid):
    try:
        import json
        import csv
        data= json.loads(coinid.body)  
        temp_coin=data['h'] #naming the key as h while accepting the json data-POST method
        coin_name=str(temp_coin).lower()
        #schedule.every(2).day.at('00:00').do(func_api.run(coin_name))
        coinlist=['bitcoin','ethereum','ripple']
        if coin_name not in coinlist:
            coin_name='bitcoin'
        func_api.run(coin_name)
        
        f= open(f'{coin_name}.csv',"r") 
        reader=csv.reader(f)
        people={}

        for row in reader:
            people[row[0]]={'magnitude':row[1]}

        return JsonResponse(people)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

    
     
    
    
