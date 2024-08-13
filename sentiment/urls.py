from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 기본 페이지 URL
    path('reddit', views.get_recent_reddit_posts, name='reddit'),
]