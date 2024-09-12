# Sentiment API

An API that provides sentiment analysis for various purposes, with a focus on finance. This API is designed to help users analyze the sentiment around assets, stocks, cryptocurrencies, and more using data from social media and other sources.

## Features
- **Keyword-based Sentiment Analysis**: Analyze sentiment based on specific keywords.
- **Media Link Analysis**: Perform sentiment analysis on articles and media content based on URLs.

## Example Usage

### 1. Sentiment Analysis by Keyword
Request sentiment analysis for a particular keyword (e.g., BTC):
```bash
GET /api/v1/sentiment/query?keyword=btc
```
Response
```bash
{
    "keyword": "btc",
    "sentiment": "positive",
    "sentiment_score": 0.85
}
```
