import sqlite3, os

cwd = os.getcwd()
db_path = os.path.join(cwd, 'url-shortner.sqlite3')

def add_link(short_link, long_link, owner):
	try:
		if not is_short_link_valid(short_link):
			raise Exception('Short link conflict')
		conn = sqlite3.connect(db_path)
		c = conn.cursor()
		params = (short_link, long_link, owner)
		c.execute('''
						INSERT INTO links(short_link, long_link, owner) VALUES(?,?,?) 
						''', params)

		conn.commit()
		conn.close()
		return True
	except Exception as e:
		print(e)

def get_link(short_link):
	try:
		conn = sqlite3.connect(db_path)
		c = conn.cursor()
		params = (short_link,)
		c.execute('''
						SELECT long_link FROM links WHERE short_link = (?) AND is_active = 1
						''', params)
		res = c.fetchall()
		conn.commit()
		conn.close()
		if len(res) == 1:
			return res[0][0]
		else:
			return None
	except Exception as e:
		print(e)

def is_short_link_valid(short_link):
	try:
		conn = sqlite3.connect(db_path)
		c = conn.cursor()
		params = (short_link,)
		c.execute('''
						SELECT long_link FROM links WHERE short_link= (?) 
						''', params)
		res = c.fetchall()
		conn.commit()
		conn.close()
		if len(res) == 0:
			return True
		else:
			return False
	except Exception as e:
		print(e)
		
def create_user(username, password_hash):
	try:
		conn = sqlite3.connect(db_path)
		c = conn.cursor()
		params = (username, password_hash)
		c.execute('''
						INSERT INTO users(username, password_hash) VALUES(?,?) 
						''', params)

		conn.commit()
		conn.close()
		return True
	except Exception as e:
		print(e)

def login_user(username):
	try:
		conn = sqlite3.connect(db_path)
		c = conn.cursor()
		params = (username,)
		c.execute('''
						SELECT username, password_hash, id FROM users WHERE username = (?) 
						''', params)
		res = c.fetchall()
		conn.commit()
		conn.close()
		if len(res) == 1:
			return res[0][0], res[0][1], res[0][2]
		else:
			return None, None, None
	except Exception as e:
		print(e)

def increment_count(short_link):
	try:
		conn = sqlite3.connect(db_path)
		cur = conn.cursor()
		params = (short_link,)
		res = cur.execute('''
						UPDATE links SET clicks = clicks + 1 WHERE short_link = (?)  AND is_active = 1
						''', params)
		conn.commit()
		conn.close()
	except Exception as e:
		print(e)

def check_user_present(username):
	try:
		conn = sqlite3.connect(db_path)
		c = conn.cursor()
		params = (username,)
		c.execute('''
						SELECT username FROM users WHERE username = (?) 
						''', params)
		res = c.fetchall()
		if len(res) > 0:
			return True
		else:
			return False
	except Exception as e:
		print(e)


def get_analysis(user_id):
	try:
		conn = sqlite3.connect(db_path)
		c = conn.cursor()
		params = (user_id,)
		c.execute('''
						SELECT * FROM links WHERE owner = (?)
						''', params)
		res = c.fetchall()
		return res
	except Exception as e:
		print(e)


def delete_link(short_link):
	try:
		conn = sqlite3.connect(db_path)
		c = conn.cursor()
		params = (short_link,)
		c.execute('''
						DELETE FROM links WHERE short_link = (?) 
						''', params)

		conn.commit()
		conn.close()
		return True
	except Exception as e:
		print(e)
		return False

def activeToggle(short_link, status):
	try:
		conn = sqlite3.connect(db_path)
		cur = conn.cursor()
		params = (status, short_link)
		res = cur.execute('''
						UPDATE links SET is_active = (?) WHERE short_link = (?)
						''', params)
		conn.commit()
		conn.close()
		return True, params[0]
	except Exception as e:
		print("Exception : ",e)
		return False, None
