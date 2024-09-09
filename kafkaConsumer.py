from kafka import KafkaConsumer, KafkaProducer
import json

# Kafka consumer setup for `Raw` topic
RAW_TOPIC_NAME = "Raw"
SENTIMENT_TOPIC_NAME = "SENTIMENT"
consumer = KafkaConsumer(
    RAW_TOPIC_NAME,
    bootstrap_servers="kafka-29db5c3-umbc-d5c9.d.aivencloud.com:16304",
    client_id="CONSUMER_CLIENT_ID",
    group_id="CONSUMER_GROUP_ID",
    security_protocol="SSL",
    ssl_cafile="ca.pem",
    ssl_certfile="service.cert",
    ssl_keyfile="service.key",
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Kafka producer setup for `SENTIMENT` topic
producer = KafkaProducer(
    bootstrap_servers="kafka-29db5c3-umbc-d5c9.d.aivencloud.com:16304",
    security_protocol="SSL",
    ssl_cafile="ca.pem",
    ssl_certfile="service.cert",
    ssl_keyfile="service.key",
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Poll messages from Kafka `Raw` topic and send to `SENTIMENT` topic
for message in consumer:
    data = message.value
    user = data.get("user", "unknown")
    polarity = data.get("polarity", 0.0)

    sentiment_message = {
        "user": user,
        "polarity": polarity
    }
    producer.send(SENTIMENT_TOPIC_NAME, sentiment_message)
    producer.flush()
    print(f"Processed message from {user}: Polarity {polarity}")

producer.close()

