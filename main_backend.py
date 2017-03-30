import usernamevalidator
import comment_processing
import praw
from datetime import datetime, timedelta
from database_things import addtodb, updatedb, finder, fetcher


reddit = praw.Reddit(client_id='JLn24zAHmQ3iPg',
                     client_secret='KnsAYz4tTBdSpX7LMB1KbjG998M',
                     user_agent='windows:com.top word finder.XD:v0.2 by /u/waitingforcracks',
                     username='waitingforcracks',
                     password='1011sailboat')

print('Read only:', reddit.read_only)  # Check if read_only
print('Ok')


def data_refetch(redditor, sorty):
    pass


def addtodbcaller(redditor, word, word_count, sorty):

    if sorty == 'top':
        addtodb(redditor, 'most_common_word_top', 'most_common_word_count_top', word, word_count, sorty)
        return True
    elif sorty == 'new':
        addtodb(redditor, 'most_common_word_new', 'most_common_word_count_new', word, word_count, sorty)
        return True
    elif sorty == 'controversial':
        addtodb(redditor, 'most_common_word_controversial', 'most_common_word_count_controversial', word, word_count, sorty)
        return True
    elif sorty == 'hot':
        addtodb(redditor, 'most_common_word_hot', 'most_common_word_count_hot', word, word_count, sorty)
        return True
    else:
        return False


def updatedbcaller(redditor, word, word_count, sorty):
    if sorty == 'top':
        updatedb(redditor, 'most_common_word_top', 'most_common_word_count_top', word, word_count, sorty)
        return True
    elif sorty == 'new':
        updatedb(redditor, 'most_common_word_new', 'most_common_word_count_new', word, word_count, sorty)
        return True
    elif sorty == 'controversial':
        updatedb(redditor, 'most_common_word_controversial', 'most_common_word_count_controversial', word, word_count, sorty)
        return True
    elif sorty == 'hot':
        updatedb(redditor, 'most_common_word_hot', 'most_common_word_count_hot', word, word_count, sorty)
        return True
    else:
        return False


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
        raise Exception('Unknown Sorting')

    return comments


def main_backend(redditor, sorty):

    record = finder(redditor)

    timesinceupdate = datetime.utcnow() - record['last_updated']

    if record is not None and timesinceupdate < timedelta(0, 86400):
        if sorty in record['sorty']:
            return fetcher(record, sorty)
        else:
            comment_contructor = comments_all(redditor=redditor, sorty=sorty)
            word_dict, comment_count = comment_processing.word_finder(comment_contructor)

            word = max(word_dict, key=word_dict.get)
            word_count = word_dict[word]

            if updatedbcaller(redditor, word, word_count, sorty):
                print('added', redditor)
            else:
                print('error adding to databaes')

            return word, word_count, comment_count

    elif record is not None and timesinceupdate > timedelta(0, 7200):
        record = data_refetch(redditor, sorty)
        # to be continued

    elif record is None:
        if usernamevalidator.username_validation(reddit=reddit, username=redditor):
            comment_contructor = comments_all(redditor=redditor, sorty=sorty)
            word_dict, comment_count = comment_processing.word_finder(comment_contructor)

            word = max(word_dict, key=word_dict.get)
            word_count = word_dict[word]

            if addtodbcaller(redditor, word, word_count, sorty):
                print('added', redditor)
            else:
                print('error adding to databaes')

            return word, word_count, comment_count
