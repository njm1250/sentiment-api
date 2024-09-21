from decouple import config  # 환경 변수 관리
import praw  # Reddit API 클라이언트
from datetime import datetime
import math
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline  # Hugging Face
import torch
from newspaper import Article
import re

model_dir = "./models/distilbert" 
model = AutoModelForSequenceClassification.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # GPU 사용 가능시 CUDA

# 파이프라인 생성
sentiment_analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1)

client_id = config('REDDIT_CLIENT_ID')  
client_secret = config('REDDIT_SECRET')  
user_agent = config('REDDIT_USER_AGENT')

def get_recent_reddit_posts(subreddit_name, search_term, post_limit, time_period):  
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
    count = 0 
    
    for post in posts:
        content = post.get('content', '')
        if not content:  # content가 비어 있거나 None인 경우 건너뜀
            continue
        
        try:
            preprocessed_text = preprocess_text(content) 
            sentiment_score = analyze_sentiment(preprocessed_text, post['score'])  
            total_sentiment += sentiment_score
            count += 1  
        except Exception as e:
            print(f"Error processing post: {e}")
            continue  
    
    return total_sentiment / count if count > 0 else 0  

def analyze_sentiment(content, score):
    # 최대 입력 길이 
    max_length = 512
    truncated_content = content[:max_length]
    
    result = sentiment_analyzer(truncated_content)
    
    sentiment_score = result[0]['score'] if result[0]['label'] == 'POSITIVE' else -result[0]['score']

    # log함수로 가중치 조정 (score = upvote - downvote)
    weighted_sentiment = sentiment_score * (1 + 0.1 * math.log1p(score))

    return weighted_sentiment

def analyze_link(link):
    try:
        article = Article(link)
        article.download()
        article.parse()
        text = article.text
    except Exception as e:
        return {'error': f'Failed to extract text from the link. Error: {str(e)}'}

    # 텍스트가 추출되지 않은 경우
    if not text:
        return {'error': 'No text found at the provided link.'}

    preprocessed_text = preprocess_text(text)

    sentiment_score = analyze_sentiment(preprocessed_text, score=0)  # score를 0으로 설정 (뉴스에는 upvote, downvote가 없기 때문에)
    
    return {
        'link': link,
        'sentiment_score': sentiment_score
    }

def preprocess_text(text):
    # 1. 소문자 변환
    text = text.lower()
    
    # 2. 특수 문자 및 불필요한 공백 제거
    text = re.sub(r'[^a-z0-9\s]', '', text)  # 알파벳 소문자, 숫자, 공백만 남기기
    text = re.sub(r'\s+', ' ', text).strip()  # 여러 개의 공백을 하나로 줄이고, 양쪽 공백 제거
    
    # 3. 반복되는 문자 제거 
    text = re.sub(r'(.)\1{2,}', r'\1', text)  # 예: "soooo" -> "so"
    
    return text
