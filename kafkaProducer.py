import nltk
from textblob import TextBlob
from kafka import KafkaProducer
import requests
import json

# Download necessary NLTK corpora
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("brown")

# Kafka producer setup
RAW_TOPIC_NAME = "Raw"
producer = KafkaProducer(
    bootstrap_servers="kafka-29db5c3-umbc-d5c9.d.aivencloud.com:16304",
    security_protocol="SSL",
    ssl_cafile="ca.pem",
    ssl_certfile="service.cert",
    ssl_keyfile="service.key",
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def analyze_sentiment(text):
    """
    Analyzes the sentiment polarity of a given text.
    
    Args:
        text (str): The text to analyze.
    Returns:
        float: Polarity of the text.
    """
    blob = TextBlob(text)
    return round(blob.sentiment.polarity, 2)

def fetch_latest_tweet():
    """
    Fetches the latest tweet from a given API endpoint.
    
    Returns:
        dict: A dictionary containing the user and tweet content.
    """
    try:
        response = requests.get("http://127.0.0.1:5000/api/latest_tweet")
        response.raise_for_status()
        tweet_data = response.json()
        if tweet_data["content"]:
            return {"user": tweet_data["user"], "content": tweet_data["content"]}
        else:
            return None
    except requests.RequestException as e:
        print(f"Error fetching latest tweet: {e}")
        return None

def send_latest_tweet():
    """
    Fetches the latest tweet, analyzes its sentiment, and sends it to the Kafka topic.
    """
    tweet_data = fetch_latest_tweet()
    if tweet_data:
        polarity = analyze_sentiment(tweet_data["content"])
        message = {
            "user": tweet_data["user"],
            "polarity": polarity
        }
        producer.send(RAW_TOPIC_NAME, message)
        producer.flush()
        print(f"Message sent: {message}")
    else:
        print("No latest tweet found.")

if __name__ == "__main__":
    send_latest_tweet()
    producer.close()
