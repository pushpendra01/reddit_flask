import pymongo
from datetime import datetime

client = pymongo.MongoClient()
database = client.reddit


def updatedb(redditor, word, word_count, comment_count, sorty):
    collection = database['word_analysis']
    # if sorty not in record['sorted_by'], add that to database
    # else if sorty in record['sorted_by'], updated that record
    record = record_finder(redditor)
    if sorty in record['sorty']:
        try:
            # modify record with new info and increase updated times by 1
            collection.update_one(
                {"redditor": redditor},
                {
                    "$set":
                    {
                        'common_word_' + sorty: word,
                        'common_word_count_' + sorty: word_count,
                        'last_updated_' + sorty: datetime.utcnow(),
                        'total_comments' + sorty: comment_count
                    },
                    "$inc":
                        {
                            'updated_times_' + sorty: 1
                        }
                }
            )

            return True
        except Exception as ex:
            print(type(ex))
            print('error in updatedb when sorty in sorty')
    elif sorty not in record['sorty']:
        try:
            collection.update_one(
                {"redditor": redditor},
                {
                    "$set":
                        {
                            'common_word_' + sorty: word,
                            'common_word_count_' + sorty: word_count,
                            'last_updated_' + sorty: datetime.utcnow(),
                            'total_comments' + sorty: comment_count
                        },
                    "$inc":
                        {
                            'updated_times_' + sorty: 1
                        },
                    "$addToSet:":
                        {
                            'sorted_by': sorty
                        }
                }
            )
        except Exception as ex:
            print(type(ex))
            print('error in updatedb when sorty not in sorty')


def addtodb(redditor, word, word_count, comment_count, sorty):
    collection = database['word_analysis']
    if sorty == 'top' or 'new' or 'conterversial' or 'hot':
        try:
            post = {'redditor': redditor,
                    'common_word_' + sorty: word,
                    'common_word_count' + sorty: word_count,
                    'total_comments' + sorty: comment_count,
                    'sorted_by': [sorty],
                    'last_updated_' + sorty: datetime.utcnow(),
                    'add_on': datetime.utcnow(),
                    'updated_times_' + sorty: 1
                    }

            collection.insert_one(post)
            return True
        except pymongo.errors.DuplicateKeyError:
            return False
    else:
        raise Exception('Unknown sorting in addtodb')


def record_finder(redditor):
    collection = database['word_analysis']
    return collection.find_one({'redditor': redditor})


def fetcher(record, sorty):
    if sorty == 'top' or 'new' or 'conterversial' or 'hot':
        return record['common_word_' + sorty], record['common_word_count_' + sorty], record['comment_count_' + sorty]
    else:
        return False
