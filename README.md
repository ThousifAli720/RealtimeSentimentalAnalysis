# Twitter-sentimental-Analysis
Project Overview:
The Real-time Twitter Sentiment Analysis project is a comprehensive system for collecting, processing, and analyzing tweets to determine the sentiments expressed in them. The solution involves deploying the default Neo4j graph database containing Twitter data, enhancing it with user-defined nodes and relationships, and analyzing tweet sentiments in real-time using NLP techniques.

Main Components:
Graph Database Setup:
Deploy Neo4j and set up the default Twitter database.
Understand the Data Model used in Neo4j, including node labels ("User," "Hashtag," etc.) and relationships ("USING," "FOLLOWS," etc.).
Prepare Queries:
Extract the list of users and hashtags.
Select specific users and hashtags for the demo.
Prepare a test dataset of tweets containing the selected hashtags and users.
Graph Queries (Cypher):
Insertion Queries:
Insertion queries to add additional users, hashtags, tweets, and relationships.
Recommendation Queries:
Queries to recommend new users to follow based on common interests or similar hashtags.
Sentiment Update Queries:
Queries to update the sentiments on appropriate nodes after processing via Kafka.

Sentiment Analysis Pipeline:
NLP Library: Use TextBlob or NLTK for sentiment classification.
Streaming Engine:
Kafka Streams or Spark Streaming (using Structured Streaming API).
Sentiment Analysis Process:
Stream tweets via Kafka message broker.
Classify sentiments (positive, neutral, negative) using NLP techniques.
Write results to the SENTIMENT Kafka topic.
Kafka Integration:
Producer: Stream raw tweets to Kafka topics.
Consumer: Process the tweets, classify sentiments, and write results to SENTIMENT topic.
Neo4j Kafka Connector:
Configure Neo4j Kafka connector as a sink to update the appropriate nodes with sentiments.

Technologies:

Backend:
Flask for web serving.
Kafka (with confluent_kafka) for message processing.
Neo4j for graph data storage and querying.
MongoDB for additional user profile and tweet storage.

NLP Libraries:
TextBlob or NLTK for sentiment analysis.

Other Libraries:
pymongo for MongoDB integration.
requests for API calls.
json for data manipulation.

Deliverables:

Neo4j Setup:
Deployed Neo4j graph database and loaded Twitter dataset.
Validated graph queries for extraction, recommendation, and sentiment updates.

MongoDB Schema:
Designed schema for user profiles and tweets.
Populated with sample data.

Kafka Sentiment Pipeline:
Implemented producer and consumer applications using Kafka.
Configured Neo4j Kafka Connector for sentiment updates.

Sentiment Analysis:
Integrated an NLP library for sentiment analysis.
Classified and processed sentiments for streamed tweets.

Web Application:
Built a Flask web application to visualize recommendations and sentiment results.
Provided CSS-styled templates for a professional look.
