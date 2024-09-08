from decouple import config  # 환경 변수 관리
import praw  # Reddit API 클라이언트
from datetime import datetime
import math
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline  # Hugging Face
import torch

model_dir = "./models/distilbert" 
model = AutoModelForSequenceClassification.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # GPU 사용 가능시 CUDA

# 파이프라인 생성
sentiment_analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1)


def get_recent_reddit_posts(subreddit_name, search_term, post_limit, time_period):
    client_id = config('REDDIT_CLIENT_ID')  
    client_secret = config('REDDIT_SECRET')  
    user_agent = config('REDDIT_USER_AGENT')  

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

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
        total_sentiment += analyze_sentiment(post['content'], post['score']) 
    return total_sentiment / len(posts) if posts else 0  

def analyze_sentiment(content, score):
    result = sentiment_analyzer(content)
    
    sentiment_score = result[0]['score'] if result[0]['label'] == 'POSITIVE' else -result[0]['score']

    # log함수로 가중치 조정 (score = upvote - downvote)
    weighted_sentiment = sentiment_score * (1 + 0.1 * math.log1p(score))

    return weighted_sentiment

def preprocess():
    # 필요시 전처리 작업 수행
    return 0
