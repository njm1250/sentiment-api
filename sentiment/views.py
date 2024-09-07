from django.shortcuts import render
from django.http import HttpResponse
from . import services

def index(request):
    posts = services.get_recent_reddit_posts('cryptocurrency', 'btc', 100, 'day')
    avg_sentiment = services.calculate_avg_sentiment(posts)

    ans = ''
    for post in posts:
        ans += post['content']
    
    return HttpResponse('Avg Score: ' + str(avg_sentiment) + ans)