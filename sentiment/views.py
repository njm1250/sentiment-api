from django.shortcuts import render
from django.http import JsonResponse
from . import services

def query(request):
    keyword = request.GET.get('keyword')
    timeframe = request.GET.get('timeframe', 'day') 
    
    if not keyword:
        return JsonResponse({'error': 'Keyword parameter is required.'}, status=400)

    posts = services.get_recent_reddit_posts('all', keyword, 10, timeframe)
    sentiment_score = services.calculate_avg_sentiment(posts)

    response_data = {
        'keyword': keyword,
        'sentiment_score': sentiment_score
    }
    
    return JsonResponse(response_data)