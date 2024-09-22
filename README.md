# Sentiment API

An API that provides sentiment analysis for various purposes. It helps users understand the sentiment around topics such as stocks and cryptocurrencies using data from social media. Currently, the data comes exclusively from Reddit.

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/sentiment-api.git
   cd sentiment-api
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the root directory and add your Reddit API credentials:
   ```env
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_SECRET=your_secret
   REDDIT_USER_AGENT=your_user_agent
   ```

5. **Run the server locally**:
   ```bash
   python manage.py runserver
   ```

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
  
### Usage Tips
- This feature works best with static content such as news articles or blog posts.
- Dynamic content like social media posts or pages with JavaScript-rendered content may not be parsed correctly.

## Limitations
- **Currently, only English language content is supported.**
- The API rate limit is set to 100 requests per hour per IP.
- Each request can analyze a maximum of 512 characters per input. Texts longer than this limit will be truncated before analysis.
