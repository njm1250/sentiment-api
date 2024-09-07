from django.test import TestCase
from sentiment import services

class SentimentTest(TestCase):
    def test_sentiment(self):
        posts = services.get_recent_reddit_posts('stocks', 'tesla', 100, 'day')
        avg_sentiment = services.calculate_avg_sentiment(posts)

        ans = ''
        for post in posts:
            ans += post['selftext']
        print("avg score: " + str(avg_sentiment) + ans)

