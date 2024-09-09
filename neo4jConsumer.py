from kafka import KafkaConsumer
from neo4j import GraphDatabase, basic_auth
import json

# Kafka consumer setup for `SENTIMENT` topic
SENTIMENT_TOPIC = "SENTIMENT"
consumer = KafkaConsumer(
    SENTIMENT_TOPIC,
    bootstrap_servers="kafka-29db5c3-umbc-d5c9.d.aivencloud.com:16304",
    client_id="CONSUMER_CLIENT_ID",
    group_id="CONSUMER_GROUP_ID",
    security_protocol="SSL",
    ssl_cafile="ca.pem",
    ssl_certfile="service.cert",
    ssl_keyfile="service.key",
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Neo4j connection setup
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "123456789"

driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_USERNAME, NEO4J_PASSWORD))

def store_sentiment(user, polarity):
    """
    Stores the user and polarity sentiment in Neo4j graph database.

    Args:
        user (str): The username.
        polarity (float): Sentiment polarity.
    """
    with driver.session() as session:
        cypher_query = """
        MERGE (u:User {screen_name: $user})
        SET u.polarity = $polarity
        """
        session.run(cypher_query, user=user, polarity=polarity)

# Poll messages from Kafka `SENTIMENT` topic and store in Neo4j
for message in consumer:
    data = message.value
    user = data["user"]
    polarity = data["polarity"]
    store_sentiment(user, polarity)
    print(f"Stored {user} with polarity {polarity} in Neo4j")

driver.close()
