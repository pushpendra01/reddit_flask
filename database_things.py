import pymongo
from datetime import datetime

client = pymongo.MongoClient()
database = client.reddit


def updatedb(redditor, word, count, sorty):
    collection = database['word_analysis']
    try:
        collection.update_one(
            {"redditor": redditor},
            {
                "$set":
                {
                    'common_word_' + sorty: word + '_' + sorty,
                    'common_word_count_' + sorty: count + '_' + sorty,
                    "last_updated": datetime.utcnow()
                }
            }
        )

        return True
    except Exception as ex:
        return ex


def addtodb(redditor, word, word_count, comment_count, sorty):
    collection = database['word_analysis']
    try:
        post = {'redditor': redditor,
                'common_word_' + sorty: word,
                'common_word_count' + sorty: word_count,
                'total_comments' + sorty: comment_count,
                'sorted_by': [sorty],
                'last_updated': datetime.utcnow(),
                'updated_times': 1
                }

        _ = collection.insert_one(post).inserted_id
        return True
    except pymongo.errors.DuplicateKeyError:
        return False


def record_finder(redditor):

    collection = database['word_analysis']
    return collection.find_one({'redditor': redditor})


def fetcher(record, sorty):

    if sorty == 'top' or 'new' or 'conterversial' or 'hot':
        return record['common_word_' + sorty], record['common_word_count_' + sorty], record['comment_count_' + sorty]
    else:
        return False
