from django.shortcuts import render
from django.http import HttpResponse
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer # type: ignore

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