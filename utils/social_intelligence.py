import feedparser
import urllib.parse

DISASTER_KEYWORDS = [
    "flood", "storm", "cyclone",
    "heavy rain", "disaster", "damage"
]

def fetch_news(city):

    query = f"{city} disaster flood storm"
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}"

    feed = feedparser.parse(url)

    headlines = []
    for entry in feed.entries[:5]:
        headlines.append(entry.title)

    return headlines


def disaster_keyword_score(text):

    score = 0
    for word in DISASTER_KEYWORDS:
        if word in text.lower():
            score += 1

    return score


def build_social_text(city):

    headlines = fetch_news(city)

    combined = " ".join(headlines)

    keyword_score = disaster_keyword_score(combined)

    return combined, keyword_score