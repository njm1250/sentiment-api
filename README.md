# Sentiment API

An API that provides sentiment analysis for various purposes. It helps users understand the sentiment around topics such as stocks and cryptocurrencies using data from social media. Currently, the data comes exclusively from Reddit.

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
