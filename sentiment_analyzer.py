
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(message):

    # Analyze customer message
    result = analyzer.polarity_scores(message)

    score = result["compound"]

    # Classify sentiment
    if score >= 0.05:
        sentiment = "Positive"

    elif score <= -0.05:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    return {
        "sentiment": sentiment,
        "score": score
    }


# Test the analyzer
if __name__ == "__main__":

    message = input("Enter customer message: ")

    result = analyze_sentiment(message)

    print("Sentiment:", result["sentiment"])
    print("Sentiment Score:", result["score"])
