from datetime import datetime, timedelta
import praw
import pymongo

client = pymongo.MongoClient()
database = client.reddit
collection = database['word_analysis']






# reddit = praw.Reddit('XDD')
# Create authenticated reddit instance
reddit = praw.Reddit(client_id='JLn24zAHmQ3iPg',
                     client_secret='KnsAYz4tTBdSpX7LMB1KbjG998M',
                     user_agent='windows:com.top word finder.XD:v0.2 by /u/waitingforcracks',
                     username='waitingforcracks',
                     password='1011sailboat')

print('Read only:', reddit.read_only)  # Check if read_only
print('Ok')


def comment_sorting(redditor, sorty):
    if sorty == 'top':
        comments = reddit.redditor(redditor).comments.top(limit=None)
    elif sorty == 'new':
        comments = reddit.redditor(redditor).comments.new(limit=None)
    elif sorty == 'controversial':
        comments = reddit.redditor(redditor).comments.controversial(limit=None)
    elif sorty == 'hot':
        comments = reddit.redditor(redditor).comments.hot(limit=None)
    else:
        raise Exception('Unknown Sorting')

    return comments


def word(redditor, asker, sorty='top'):
    count = 0
    word_dict = {}

    record = collection.find_one({'redditor': redditor})
    if record is None:
        print('Not found')
    else:
        print(record['redditor'])

    if datetime.utcnow() - record['last_updated'] > timedelta(0, 7200) or record is None:
        # Modify to first look in valid_usernames and then reddit
        comments = comment_sorting(redditor, sorty)


        most_common_word = max(word_dict, key=word_dict.get)
        most_common_word_num = word_dict[most_common_word]



