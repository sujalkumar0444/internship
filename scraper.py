import time
import datetime
import uuid
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
# MongoDB setup

client = MongoClient(os.getenv("MONGO_URI"))
db = client.twitter_trends
collection = db.trends

with open ("valid_proxies.txt", 'r') as f:
    proxies=f.read().split("\n")

# ProxyMesh setup
# proxies = [
#  
# #     "http://username:password@host:port",
# #     "http://username:password@host:port",
# #     "http://username:password@host:port"
# ]

def fetch_trending_topics():
    # Choose a random proxy from the list


# proxy = random.choice(proxies)

# choose proxy from either valid_proxies or ProxyMesh
# set chrome settings for proxy server
    
    # Initialize WebDriver with the chosen proxy
    options = webdriver.ChromeOptions()
    #remove comment for adding proxy server , make sure to add proxy server in the chrome settings.
#     options.add_argument('--proxy-server=http=%s' % proxy)
#     options.add_argument('--proxy-server=https=%s' % proxy)
    service = Service(r'C:\Users\sujal\Downloads\chromedriver-win64\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Log in to Twitter
        driver.get("https://x.com/i/flow/login")
        username_input = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']")))

        # Enter username
        username_input.send_keys(os.getenv("TWITTER_USERNAME"))

        # Wait for the "Next" button
        next_button = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))

        # Click on the "Next" button
        next_button.click()

        # Wait for the password input field to be present
        password_input = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))

        # Enter password
        password_input.send_keys(os.getenv("TWITTER_PASSWORD"))

        # Wait for the sign-in button
        sign_in_button = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']")))

        # Click on the sign-in button
        sign_in_button.click()

        # Wait for login to complete and homepage to load
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Timeline: Trending now']")))

        # Fetch trending topics
        trends = driver.find_elements(By.CSS_SELECTOR, "div[aria-label='Timeline: Trending now'] div.css-146c3p1.r-bcqeeo.r-1ttztb7.r-qvutc0.r-37j5jr.r-a023e6.r-rjixqe.r-b88u0q.r-1bymd8e >span")
        trending_topics = [trend.text for trend in trends[:5]]

        # Generate unique ID
        unique_id = str(uuid.uuid4())

        # Record date and time
        end_time = datetime.datetime.now()

        # Store results in MongoDB
        record = {
            "_id": unique_id,
            "trend1": trending_topics[0] if len(trending_topics) > 0 else '',
            "trend2": trending_topics[1] if len(trending_topics) > 1 else '',
            "trend3": trending_topics[2] if len(trending_topics) > 2 else '',
            "trend4": trending_topics[3] if len(trending_topics) > 3 else '',
            "trend5": trending_topics[4] if len(trending_topics) > 4 else '',
            "end_time": end_time,
            "ip_address": "add proxy ip here"
            # "ip_address": proxy
        }
        collection.insert_one(record)

        # Return results for HTML page
        return record

    finally:
        driver.quit()

# For testing
if __name__ == '__main__':
    record = fetch_trending_topics()
    print(record)
