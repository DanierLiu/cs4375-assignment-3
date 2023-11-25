# Part 2

import re

old = 'bbchealth.txt'
processed_tweets = []
with open (old, 'r') as file:
    tweets = file.readlines()

for tweet in tweets:
    parts = tweet.split('|')

    if len(parts) >= 3:
        new_tweet = re.sub(r'http\S+', '', parts[2].strip()).strip()
        processed_tweets.append(new_tweet)

new_data = 'tweets.txt'

with open(new_data, 'w') as output_file:
    for tweet in processed_tweets:
        output_file.write(tweet + '\n')

# Insert the rest when done