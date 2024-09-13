from django.shortcuts import render
from django.http import JsonResponse
from . import services
from django_ratelimit.decorators import ratelimit
from django.views.decorators.cache import cache_page

@ratelimit(key='ip', rate='100/h', method='GET', block=True)
@cache_page(60 * 15)
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