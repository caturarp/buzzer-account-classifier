from flask import Flask, jsonify

import twitter
import pandas as pd
import csv
import json


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


app = Flask(__name__)

# Replace with your own Twitter API keys
api = twitter.Api(consumer_key="2CW39gBbl8RaL6ED9lUGUL3Kt",
                  consumer_secret="TiaGBqh9qUqL3Dx1bV9abI3jfMeuXfXa7Ko0xKWoioOn0DhOPm",
                  access_token_key="1520536260300787712-Rtwy55jn2E7HvQCqKqywDlF20QMXfg",
                  access_token_secret="kK8p1RFbH3WnYo1eFuTCIdIggypIrQrIIj2PXaVTaBW18")

# # create a csv file, expect data from twitter
def create_csv(data):

    #convert response to string
    passed_data = data.get_data()
    print(passed_data)

    #convert string to json
    loaded_data = json.loads(passed_data)
    print(loaded_data)
    
    # Open a CSV file to write the results to
    with open('dataset.csv', 'w', newline='') as csvfile:

        # Create a writer object from csv module
        writer = csv.writer(csvfile)

        # Write the column head "username" to the CSV file
        writer.writerow(["username"])

        # get a list of the "screen_name" values from the JSON data
        screen_names = [item['screen_name'] for item in loaded_data]
        
        # join the screen_names with commas
        screen_names_str = ','.join(screen_names)
        
        # write the screen_names_str to the CSV file
        writer.writerow([screen_names_str])

    return "success"

# create a csv file from hashtag
# def create_csv_hashtag(data):
    
#         # Create a csv.writer object
#         writer = csv.writer(open("dataset.csv", "w"))
        
#         # Write the column head "username" to the CSV file
#         writer.writerow(["username"])

#         #


# Fetch the user's timeline
@app.route('/tweets/<username>')
def get_tweets(username):
    # Fetch the user's tweets
    tweets = api.GetUserTimeline(screen_name=username)
    analyzer = SentimentIntensityAnalyzer()
    
    # Convert the tweets to a list of dictionaries
    tweets_data = [{"text": tweet.text} for tweet in tweets]
    # tweets_data = [{"text": tweet.text, "created_at": tweet.created_at} for tweet in tweets]
    
    # Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(tweets_data, columns=['text'])

    # Preprocess the tweets by removing the username
    df['text'] = df['text'].str.replace(r'@[\w]+', '')
    
    # Print the first few rows of the DataFrame
    print(df.head())

    # Perform sentiment analysis on the tweets
    df['scores'] = df['text'].apply(lambda text: analyzer.polarity_scores(text))
    df['compound']  = df['scores'].apply(lambda score_dict: score_dict['compound'])

    print(df.head())

    # Return the tweets as JSON
    return df.to_json(orient='records')

# Fetch the user's followers
@app.route('/followers/<username>')
def get_followers(username):
    # Fetch the user's followers
    followers = api.GetFollowers(screen_name=username)
    
    # Convert the followers to a list of dictionaries
    followers_data = [{"name": follower.name, "screen_name": follower.screen_name} for follower in followers]
    # Return the followers as JSON
    return jsonify(followers_data, len(followers_data))

# Fetch the user's followers count
@app.route('/followers/count/<username>')
def get_followers_count(username):
    # Fetch the user's followers count
    followers_count = api.GetFollowerIDs(screen_name=username)
    # print(followers_count)
    return jsonify(len(followers_count))

# Fetch the user's friends
@app.route('/friends/<username>')
def get_friends(username):
    # Fetch the user's friends
    friends = api.GetFriends(screen_name=username)
    
    # Convert the friends to a list of dictionaries
    friends_data = [{"name": friend.name, "screen_name": friend.screen_name} for friend in friends]
    
    # Return the friends as JSON
    return jsonify(friends_data, len(friends_data))

# Fetch the user's following count
@app.route('/friends/count/<username>')
def get_following_count(username):
    # Fetch the user's following count
    following_count = api.GetFriendIDs(screen_name=username)
    return jsonify(len(following_count))

# Fetch the user's account creation date
@app.route('/account/created/<username>')
def get_account_created(username):
    # Fetch the user's account creation date
    account_created = api.GetUser(screen_name=username).created_at
    return jsonify(account_created)

# Fetch list of username that discuss about specific hashtag and create a csv file
@app.route('/hashtag/<hashtag>')
def get_hashtag(hashtag):
    # Fetch the user that discuss about specific hashtag
    hashtag = api.GetSearch(raw_query="q=%23"+hashtag+"&src=typed_query&f=live")
    # print(hashtag)
    hashtag_data = [{"screen_name": hashtag.user.screen_name} for hashtag in hashtag]
    # return jsonify(hashtag_data)
    
    return create_csv(jsonify(hashtag_data))


if __name__ == '__main__':
    app.run()