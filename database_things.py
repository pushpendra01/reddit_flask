import pymongo
from datetime import datetime

client = pymongo.MongoClient()
database = client.reddit


def updatedb(redditor, most_common_word_type, most_common_word_count_type, word_type, count_type):
    collection = database['word_analysis']
    try:
        collection.update_one(
            {"redditor": redditor},
            {
                "$set":
                {
                    most_common_word_type: word_type,
                    most_common_word_count_type: count_type,
                    "last_updated": datetime.utcnow()
                }
            }
        )

        return True
    except Exception as ex:
        return ex


def addtodb(redditor, most_common_word_type, most_common_word_count_type, word_type, count_type, sorty):
    collection = database['word_analysis']
    try:
        post = {'redditor': redditor,
                most_common_word_type: word_type,
                most_common_word_count_type: count_type,
                'sorty': [sorty],
                "last_updated": datetime.utcnow()
                }

        _ = collection.insert_one(post).inserted_id
        return True
    except pymongo.errors.DuplicateKeyError:
        return False


def finder(redditor):

    collection = database['word_analysis']
    return collection.find_one({'redditor': redditor})


def fetcher(record, sorty):

    if sorty == 'top':
        return record['most_common_word_' + sorty]
        return record['most_common_word_top'], record['most_common_word_count_top'], record['comment_count_top']
    elif sorty == 'new':
        return record['most_common_word_new'], record['most_common_word_count_new'], record['comment_count_new']
    elif sorty == 'controversial':
        return record['most_common_word_controversial'], record['most_common_word_count_controversial'], record['comment_count_controversial']
    elif sorty == 'hot':
        return record['most_common_word_hot'], record['most_common_word_count_hot'], record['comment_count_hot']
    else:
        return False

# def fetcher(record, sorty, x):


def updatedb(redditor, most_common_word_type, most_common_word_count_type, word_type, count_type, sorty):
    collection = database['word_analysis']
    try:
        post = {'redditor': redditor,
                most_common_word_type: word_type,
                most_common_word_count_type: count_type,
                'sorty': [sorty],
                "last_updated": datetime.utcnow()
                }

        _ = collection.insert_one(post).inserted_id
        return True
    except pymongo.errors.DuplicateKeyError:
        return False


