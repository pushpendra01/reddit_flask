from datetime import datetime, timedelta

# Package import
import praw

# Local Import
import comment_processing
import database_things
import usernamevalidator


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
	print('hmm')
	time_since_update = 0
	record = database_things.record_finder(redditor)
	try:
		time_since_update = datetime.utcnow() - record['last_updated' + sorty]
		print(time_since_update)
		print('ok')
	except Exception as ex:
		print(type(ex))
		pass

	# if redditor is already in database
	if record is not None:
		# and it is less than 2hrs

		if time_since_update < timedelta(0, 86400):
			# and this particular sorting is in the database
			if sorty in record['sorted_by']:
				return database_things.data_fetcher(record, sorty)
			elif sorty not in record['sorted_by']:
				word, word_count, comment_count = data_fetch(redditor, sorty)
				try:
					database_things.updatedb(redditor, word, word_count, comment_count, sorty)
				except Exception as ex:
					print(type(ex))
				finally:
					return word, word_count, comment_count

		elif time_since_update >= timedelta(0, 86400):

			word, word_count, comment_count = data_fetch(redditor, sorty)
			try:
				database_things.updatedb(redditor, word, word_count, comment_count, sorty)
			except Exception as ex:
				print(type(ex))


	elif record is None:
		if usernamevalidator.username_validation(reddit=reddit, username=redditor):
			word, word_count, comment_count = data_fetch(redditor, sorty)

			try:
				database_things.addtodb(redditor, word, word_count, comment_count, sorty)
				print('added', 'new', redditor, 'to database')
			except Exception as ex:
				print(type(ex))
				print('error adding to databaes new redditor ')
			finally:
				return word, word_count, comment_count
