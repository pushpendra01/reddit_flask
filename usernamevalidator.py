import prawcore


def username_validation(reddit, username):
	try:
		_ = reddit.redditor(username).id
		return True
	except prawcore.exceptions.NotFound:
		return False
