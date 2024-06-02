from flask import Flask, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from scraper import fetch_trending_topics
import os
from dotenv import load_dotenv


load_dotenv()



app = Flask(__name__)
CORS(app)

# Initialize existing_records as a global variable
existing_records = []

# Function to fetch existing records from the database
def fetch_existing_records():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client.twitter_trends
    collection = db.trends
    return list(collection.find({}))

@app.route('/load_records')
def load():
    global existing_records
    existing_records = fetch_existing_records()
    return jsonify(existing_records)

# Route to fetch existing records when the page is loaded
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch new records when the button is clicked
@app.route('/run_script')
def run_script():
    global existing_records
    existing_records = fetch_existing_records()
    new_record = fetch_trending_topics()  # Fetch a new record
    existing_records.append(new_record)  # Add the new record to the existing ones
    return jsonify(existing_records)

if __name__ == '__main__':
    app.run(debug=True)
