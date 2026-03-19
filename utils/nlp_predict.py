import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon', quiet=True)

sia = SentimentIntensityAnalyzer()

def predict_text_risk(text):

    score = sia.polarity_scores(text)

    negative = score["neg"]

    disaster_keywords = [
        "flood", "storm", "cyclone", "rain",
        "damage", "evacuation", "alert"
    ]

    boost = 0
    for word in disaster_keywords:
        if word in text.lower():
            boost += 0.1

    risk = min(1.0, negative + boost)

    return float(risk)