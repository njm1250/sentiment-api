from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer # type: ignore
from datetime import datetime, timedelta
from decouple import config
import praw

def get_recent_reddit_posts(request):
    client_id = config('REDDIT_CLIENT_ID')  
    client_secret = config('REDDIT_SECRET')  
    user_agent = config('REDDIT_USER_AGENT')  

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    # 서브레딧
    subreddit = reddit.subreddit('cryptocurrency')
    query = "xrp"  

    posts = []
    for submission in subreddit.search(query, limit=10, time_filter='day'):
        post_time = datetime.utcfromtimestamp(submission.created_utc)
        posts.append({
            'title': submission.title,
            'selftext': submission.selftext,
            'created': post_time.strftime('%Y-%m-%d %H:%M:%S'),
        })

    return JsonResponse({'posts': posts})

def index(request):
    # 분석할 문장
    sentence = "Yo I'm so Excited about the Tesla right now."

    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(sentence)

    if vs['compound'] > 0:
        sentiment = 'Positive'
    elif vs['compound'] == 0:
        sentiment = 'Neutral'
    else:
        sentiment = 'Negative'

    print(f"Compound Score: {vs['compound']}")

    # 결과를 HTTP 응답으로 반환
    return HttpResponse(sentiment)