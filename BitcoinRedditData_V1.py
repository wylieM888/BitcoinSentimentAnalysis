# ***PART 1***

import json
url = 'https://www.reddit.com/'

# For security reasons, create a JSON object with your credentials:

# {
# 	"client_id": "Use your personal use script id",
# 	"api_key": "Use the secret key",
# 	"username": "Your Reddit Username",
# 	"password": "Your reddit password"
# }

# Change to path with your credentials JSON file
with open('C:/Users/guest1/Desktop/credentials.json') as f:
    params = json.load(f)

# ***PART 2***

import praw

# Create the Praw API Reddit object using the JSON file
reddit = praw.Reddit(client_id=params['client_id'], 
                     client_secret=params['api_key'],
                     password=params['password'], 
                     # Make sure to change the user_agent name and Username
                     user_agent='reddit_explore accessAPI:v0.0.1 (by /u/Cleverthingsisaid)',
                     username=params['username'])

# ***PART 3***

# Create subreddit objects to extract data 
bitcoinReddit = reddit.subreddit('Bitcoin')

# ***PART 4***

start_date = int(1635739200) # '2021-01-30 00:00:00' in Unix time
end_date = 1614581999  # '2021-11-30 00:00:00' in Unix time

print(type(start_date))

# ***PART 5***

import pandas as pd

posts = pd.DataFrame(columns=['title', 'flair', 'score', 'upvote_ratio', 'id',
                              'subreddit', 'url', 'num_comments', 'body', 'created'])  # Dataframe to store results

# ***PART 6***

import time
import requests
import praw
from pandas import DataFrame as df

def submissions_pushshift_praw(subreddit, start, end, limit=100, extra_query=""):
    """
    A simple function that returns a list of PRAW submission objects during a particular period from a defined sub.
    This function serves as a replacement for the now deprecated PRAW `submissions()` method.
    
    :param subreddit: A subreddit name to fetch submissions from.
    :param start: A Unix time integer. Posts fetched will be AFTER this time. (default: None)
    :param end: A Unix time integer. Posts fetched will be BEFORE this time. (default: None)
    :param limit: There needs to be a defined limit of results (default: 100), or Pushshift will return only 25.
    :param extra_query: A query string is optional. If an extra_query string is not supplied, 
                        the function will just grab everything from the defined time period. (default: empty string)
    
    Submissions are yielded newest first.
    
    For more information on PRAW, see: https://github.com/praw-dev/praw 
    For more information on Pushshift, see: https://github.com/pushshift/api
    """
    matching_praw_submissions = []
    
    # Default time values if none are defined (credit to u/bboe's PRAW `submissions()` for this section)
    utc_offset = 28800
    now = int(time.time())
    start = max(int(start) + utc_offset if start else 0, 0)
    end = min(int(end) if end else now, now) + utc_offset
    
    # Format our search link properly.
    search_link = ('https://api.pushshift.io/reddit/submission/search/'
                   '?subreddit={}&after={}&before={}&sort_type=score&sort=asc&limit={}&q={}')
    search_link = search_link.format(subreddit, start, end, limit, extra_query)
    
    # Get the data from Pushshift as JSON.
    retrieved_data = requests.get(search_link)
    returned_submissions = retrieved_data.json()['data']
    
    # Iterate over the returned submissions to convert them to PRAW submission objects.
    for submission in returned_submissions:
        
        # Take the ID, fetch the PRAW submission object, and append to our list
        praw_submission = reddit.submission(id=submission['id'])
        matching_praw_submissions.append(praw_submission)
     
    # Return all PRAW submissions that were obtained.
    return matching_praw_submissions

# ***PART 7***

# Continue loop until end date is reached
while start_date:
    S = submissions_pushshift_praw(subreddit='Bitcoin',start=start_date, end=end_date, limit=10000)  # Pull posts within date range
    
    for post in S:  # Looping through each post
        try: # Try/except to catch any erroneous post pulls
            if post.selftext != '[removed]' and post.selftext != '[deleted]': # Remove the deleted posts

                    posts = posts.append(
                        {'title':post.title,
                         'flair':post.link_flair_css_class,
                         'score':post.score,
                         'upvote_ratio':post.upvote_ratio,
                         'id':post.id,
                         'subreddit':post.subreddit,
                         'url':post.url,
                         'num_comments':post.num_comments,
                         'body':post.selftext,
                         'created':post.created}, ignore_index=True)  # Retrieve post data and append to dataframe

        except:
            next()  # Continue loop if error is found

    if len(S): # To identify when the last pull is reached
        break
    start_date = posts['created'].max()  # Select the next earliest date to pull posts from
    print(start_date)  # An indicator of progress