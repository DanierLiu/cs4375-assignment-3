import matplotlib.pyplot as pp
import re
import numpy as np

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

tweet_data = []
with open("tweets.txt", "r") as f:
    lines = f.readlines()
    for l in lines: tweet_data.append(set([x.strip() for x in l.split(" ")]))
tweet_data = np.array(tweet_data)

# Insert the rest when done
def distance(a, b):
    intersect = len(a.intersection(b))
    union = len(a.union(b))
    return 1 - (intersect / union) if union != 0 else 0

def get_majority(data):
    if len(data) == 0: return set()
    x = {}
    for d in data:
        for e in d:
            x[e] = x.get(e, 0) + 1
    ans = max(x, key=x.get)
    return {ans}


def kmeans(data, k=10, max_iterations=100):
    centroids = data[np.random.choice(len(data), k, replace=False)]
    while max_iterations > 0:
        distance_array = np.array([[distance(d, c) for c in centroids] for d in data])
        assignments = np.argmin(distance_array, axis=1)
        centroids_new = np.array([get_majority(data[assignments == i]) for i in range(k)])
        if np.array_equal(centroids, centroids_new): break
        centroids = centroids_new
        max_iterations -= 1
    return centroids, assignments

table_data = []
for k in range(5, 11):
    centroids, assignments = kmeans(tweet_data, k, 10000)
    sse = 0
    for d in range(len(assignments)):
        sse += distance(tweet_data[d], centroids[assignments[d]]) ** 2

    table_data.append([k, sse, centroids, assignments])

headers = ["Value of K", "SSE", "Size of each cluster"]
celltext = []
maxheight = 0
for d in table_data:
    t = []
    k, sse = d[0:2]
    centroids, assignments = d[2:4]
    t.append(k)
    t.append(sse)
    s = ""
    di = {x: 0 for x in range(len(centroids))}
    for a in assignments:
        di[a] += 1
    for k in sorted(di.keys()):
        s += f"{k + 1}: {di[k]}\n"
    t.append(s)
    celltext.append(t)
    maxheight = max(maxheight, len(di))
table = pp.table(cellText=celltext, colLabels=headers, loc="center")
for r in range(len(celltext) + 1):
    for c in range(len(headers)):
        if r == 0: continue
        table[r, c].set_height(maxheight / 20)
ax = pp.gca()
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
pp.box(on=None)
fig = pp.gcf()
pp.savefig("table.png", bbox_inches="tight", dpi=150)