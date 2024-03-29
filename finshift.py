import requests
from bs4 import BeautifulSoup
import json
from nltk.sentiment import SentimentIntensityAnalyzer

# Function to scrape headlines from a specific website
def scrape_headlines(url, headers, tag, classes):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = soup.find_all(tag, class_=classes)  # Adjust class name or HTML structure based on the website
    return [headline.text.strip() for headline in headlines]

# Define URLs for news sources
urls = [
    'https://www.business-standard.com/finance/news',
    'https://m.economictimes.com/news/economy/finance',
    'https://www.reuters.com/business/finance/',
]

headers = [{
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 Edg/119.0.0.0',
}, {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 Edg/119.0.0.0',
}, {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 Edg/119.0.0.0',
}]

tags = ['a', 'p', 'a']
classes = ['smallcard-title', 'UAZlE', 'text__heading_6__1qUJ5']
# Scrape headlines from each URL
all_headlines = []
for url, header, tag, cls in zip(urls, headers, tags, classes):    
    all_headlines.extend(scrape_headlines(url, header, tag, cls))


# Deduplicate headlines
unique_headlines = list(set(all_headlines))

# writing headlines into a file
with open('headlines.txt', 'w', encoding='utf-8') as file:
    for headline in unique_headlines:
        file.write(headline + "\n")

# Sentiment analysis using NLTK
sia = SentimentIntensityAnalyzer()
news_sentiment = {headline: sia.polarity_scores(headline) for headline in unique_headlines}

# Store aggregated news with sentiment in JSON format
aggregated_news = [{'headline': headline, 'sentiment': sentiment} for headline, sentiment in news_sentiment.items()]

with open('financial_news.json', 'w') as file:
    json.dump(aggregated_news, file, indent=4)

print("Financial news scraped, aggregated, and stored in 'financial_news.json'.")
