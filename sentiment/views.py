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
    post_limit = int(request.GET.get('limit', 10)) 

    # 유효한 timeframe 옵션
    valid_timeframes = ['hour', 'day', 'week', 'month', 'year']
    
    if not keyword:
        return JsonResponse({'error': 'Keyword parameter is required.'}, status=400)
    
    if timeframe not in valid_timeframes:
        return JsonResponse({'error': f"Invalid timeframe. Valid options are: {', '.join(valid_timeframes)}"}, status=400)

    try:
        post_limit = int(post_limit)
        if post_limit < 1 or post_limit > 100:
            return JsonResponse({'error': 'Post limit must be between 1 and 100.'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'Post limit must be an integer.'}, status=400)

    posts = services.get_recent_reddit_posts('all', keyword, post_limit, timeframe)
    sentiment_score = services.calculate_avg_sentiment(posts)

    response_data = {
        'keyword': keyword,
        'sentiment_score': sentiment_score,
        'limit': post_limit,
        'timeframe': timeframe
    }
    
    return JsonResponse(response_data)

@ratelimit(key='ip', rate='100/h', method='GET', block=True)
@cache_page(60 * 15)
def links(request):
    link = request.GET.get('link')
    
    if not link:
        return JsonResponse({'error': 'Link parameter is required.'}, status=400)
    
    result = services.analyze_link(link)
    
    if 'error' in result:
        return JsonResponse(result, status=400)
    
    return JsonResponse(result)