from neo4j import GraphDatabase, basic_auth

def insert_tweet(username, tweet):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "123456789"))
    with driver.session() as session:
        append_hashtag = False
        mentioned_users = []
        hashtags = []
        append_mention = False

        for i in range(len(tweet)):
            if tweet[i] == " ":
                append_mention = False
                append_hashtag = False
            if append_mention:
                mentioned_users[len(mentioned_users) - 1] += tweet[i]
            if append_hashtag:
                hashtags[len(hashtags) - 1] += tweet[i]
            if tweet[i] == '@':
                append_mention = True
                mentioned_users.append("")
            if tweet[i] == '#':
                append_hashtag = True
              hashtags.append("")

        cipher_query = """
        MATCH (u: User {screen_name: $username})
        CREATE (p:Tweet {text: $tweet})
        CREATE (u)-[:POSTS]->(p)
        """
        for mentioned_user in mentioned_users:
            if mentioned_user:  # Skip empty mentions
                cipher_query += f"""
                MERGE (mu: User {{screen_name: '{mentioned_user}'}})
                CREATE (p)-[:MENTIONS]->(mu)
                """
        for hashtag in hashtags:
            if hashtag:  # Skip empty hashtags
                cipher_query += f"""
                MERGE (h:Hashtag {{name: '{hashtag}'}})
                CREATE (p)-[:TAGS]->(h)
                """
        session.run(cipher_query, username=username, tweet=tweet)
def reccomend_tweet(username):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "123456789"))
    with driver.session() as session:
        recommend_query = """
        MATCH (u:User {screen_name: $username})-[:POSTS]->(t:Tweet)-[:TAGS]->(h:Hashtag)
        WITH h
        MATCH (h)<-[:TAGS]-(t2:Tweet)<-[:POSTS]-(u2:User)
        RETURN u2.screen_name AS username
        LIMIT 10
        """
        result = session.run(recommend_query, username=username)
        return [record["username"] for record in result]

def get_polarity_recommendations(username):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "123456789"))
    with driver.session() as session:
        polarity_query = """
        MATCH (u:User {screen_name: $username})
        WHERE u.polarity IS NOT NULL
        WITH u.polarity AS user_polarity
        MATCH (other:User)
        WHERE other.polarity IS NOT NULL AND other.screen_name <> $username
        AND ((user_polarity < 0 AND other.polarity < 0) OR (user_polarity > 0 AND other.polarity > 0))
 RETURN other.screen_name AS username, other.polarity AS polarity
        ORDER BY other.screen_name
        """
        result = session.run(polarity_query, username=username)
        return [{"username": record["username"], "polarity": record["polarity"]} for record in result]
