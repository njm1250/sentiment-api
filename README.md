# Sentiment API

An API that provides sentiment analysis for various purposes. It helps users understand the sentiment around topics such as stocks and cryptocurrencies using data from social media. Currently, the data comes exclusively from Reddit.

## Features
- **Keyword-based Sentiment Analysis**: Analyze sentiment based on specific keywords.
- **Media Link Analysis**: Perform sentiment analysis on articles and media content based on URLs.

## Example Usage

### 1. Sentiment Analysis by Keyword
Request sentiment analysis for a particular keyword (e.g., BTC):
```bash
GET /api/v1/sentiment/query?keyword=btc&limit=50&timeframe=week
```
Response
```bash
{
    "keyword": "nvda",
    "sentiment_score": 0.85,
    "limit": 50,
    "timeframe": "week"
}
```
### Request Parameters

- **keyword** (required): The keyword to analyze (e.g., `btc`, `aapl`).
- **limit** (optional): The number of posts to analyze. Default is 10, and the maximum is 100.
- **timeframe** (optional): The time range to consider for the analysis. Default is `day`. Available options are:
  - `hour`: Last hour
  - `day`: Last day (default)
  - `week`: Last week
  - `month`: Last month
  - `year`: Last year
---
### 2. Sentiment Analysis by Media Link
Request sentiment analysis for a specific media link:
```bash
GET /api/v1/sentiment/links?link=https://example.com/article
```
Response:
```json
{
    "link": "https://example.com/article",
    "sentiment_score": 0.75
}
```
### Request Parameters
- **link** (required): The link to analyze (e.g., `https://example.com/article`).

## Limitations
- The API rate limit is set to 100 requests per hour per IP.
