from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from Queries import reccomend_tweet, get_polarity_recommendations

app = Flask(_name_)
app.secret_key = ' '  

client = MongoClient('localhost', 27017)
db = client.twitter_clone

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = db.users.find_one({"username": username, "password": password})
    if user:
        session['username'] = user['username']  # Store username in session
        return redirect(url_for('home'))
    else:
        return "Invalid username or password", 403

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        tweet_content = request.form['tweet']
        hashtags = extract_hashtags(tweet_content)
        db.tweets.insert_one({"content": tweet_content, "user": session['username'], "hashtags": hashtags})
        return redirect(url_for('recommendations'))

    return render_template('home.html', username=session['username'])

@app.route('/recommendations')
def recommendations():
    if 'username' not in session:
        return redirect(url_for('index'))

    username = session['username']
    recommendations = reccomend_tweet(username)
    return render_template('recommendations.html', recommendations=recommendations, username=username)

@app.route('/updated_recommendations')
def updated_recommendations():
    if 'username' not in session:
        return redirect(url_for('index'))

    username = session['username']
   polarity_recommendations = get_polarity_recommendations(username)
    return render_template('updated_recommendations.html', recommendations=polarity_recommendations, username=username)

@app.route('/api/latest_tweet')
def get_latest_tweet():
    """Get the latest tweet from the database."""
    latest_tweet = db.tweets.find_one(sort=[("_id", -1)])
    if latest_tweet:
        return {
            "content": latest_tweet["content"],
            "user": latest_tweet["user"],
            "hashtags": latest_tweet["hashtags"]
        }
    else:
        return {"content": "", "user": "", "hashtags": []}

def extract_hashtags(text):
    return [part[1:] for part in text.split() if part.startswith('#')]

if _name_ == '_main_':
    app.run(debug=True)
