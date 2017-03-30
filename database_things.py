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

    if sorty == 'top' or 'new' or 'conterversial' or 'hot':
        return record['most_common_word_' + sorty], record['most_common_word_count_' + sorty], record['comment_count_' + sorty]
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


