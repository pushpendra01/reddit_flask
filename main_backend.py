import usernamevalidator
import comment_processing
import praw
from datetime import datetime, timedelta
from database_things import addtodb, updatedb, record_finder, fetcher


reddit = praw.Reddit(client_id='JLn24zAHmQ3iPg',
                     client_secret='KnsAYz4tTBdSpX7LMB1KbjG998M',
                     user_agent='windows:com.top word finder.XD:v0.2 by /u/waitingforcracks',
                     username='waitingforcracks',
                     password='1011sailboat')

print('Read only:', reddit.read_only)  # Check if read_only
print('Ok')


def data_fetch(redditor, sorty):
    comment_contructor = comments_all(redditor=redditor, sorty=sorty)
    word_dict, comment_count = comment_processing.word_finder(comment_contructor)

    word = max(word_dict, key=word_dict.get)
    word_count = word_dict[word]

    return word, word_count, comment_count


def comments_all(redditor, sorty):
    if sorty == 'top':
        comments = reddit.redditor(redditor).comments.top(limit=None)
    elif sorty == 'new':
        comments = reddit.redditor(redditor).comments.new(limit=None)
    elif sorty == 'controversial':
        comments = reddit.redditor(redditor).comments.controversial(limit=None)
    elif sorty == 'hot':
        comments = reddit.redditor(redditor).comments.hot(limit=None)
    else:
        print(sorty)
        raise Exception('Unknown Sorting')

    return comments


def main_backend(redditor, sorty):


    time_since_update = 0
    record = record_finder(redditor)
    try:
        time_since_update = datetime.utcnow() - record['last_updated']
    except Exception as ex:
        print(type(ex))
        pass

    # if redditor is already in database
    if record is not None:
        # and it is less than 2hrs
        if time_since_update < timedelta(0, 86400):
            # data already there
            if sorty in record['sorted_by']:
                return fetcher(record, sorty)
            else:
                word, word_count, comment_count = data_fetch(redditor, sorty)
                try:
                    updatedb(redditor, word, word_count, sorty)
                except Exception as ex:
                    print(type(ex))

        elif time_since_update > timedelta(0, 7200):
            if sorty in record['sorted_by']:
                word, word_count, comment_count = data_fetch(redditor, sorty)


                # update old record
            elif sorty not in record['sorted_by']:
                word, word_count, comment_count = data_fetch(redditor, sorty)
                try:
                    updatedb(redditor, word, word_count, sorty)
                except Exception as ex:
                    print(type(ex))

    elif record is None:
        if usernamevalidator.username_validation(reddit=reddit, username=redditor):
            word, word_count, comment_count = data_fetch(redditor, sorty)



            if addtodb(redditor, word, word_count, comment_count, sorty):
                print('added', 'new', redditor, 'to database')
            else:
                print('error adding to databaes new redditor ')


            return word, word_count, comment_count
