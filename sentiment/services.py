from decouple import config # type: ignore
import praw # type: ignore
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer # type: ignore

def get_recent_reddit_posts(subreddit_name, search_term, post_limit, time_period):
    client_id = config('REDDIT_CLIENT_ID')  
    client_secret = config('REDDIT_SECRET')  
    user_agent = config('REDDIT_USER_AGENT')  

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    # 서브레딧 stocks, investing, cryptocurrency, Bitcoin, ethtrader
    subreddit = reddit.subreddit(subreddit_name)
    query = search_term 

    posts = []
    for submission in subreddit.search(query, limit=post_limit, time_filter=time_period):
        post_time = datetime.utcfromtimestamp(submission.created_utc)
        posts.append({
            'content': submission.title + submission.selftext,
            'created': post_time.strftime('%Y-%m-%d %H:%M:%S'),
            'score': submission.score
        })
    return posts

def calculate_avg_sentiment(posts):
    total_sentiment = 0
    for post in posts:
        total_sentiment += analyze_sentiment(post['content']) 
    return total_sentiment / len(posts) if posts else 0  

def analyze_sentiment(content):
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(content)
    return vs['compound']

def preprocess():
    # 전처리
    return 0