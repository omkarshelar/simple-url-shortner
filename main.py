from flask import Flask, jsonify, render_template, redirect, request, session, url_for, flash, send_from_directory
from models import add_link, is_short_link_valid, get_link, create_user, login_user, check_user_present, increment_count, get_analysis,delete_link, activeToggle
from forms import ShortenForm, SignupForm, LoginForm
import random, string, bcrypt, os

app = Flask(__name__)
app.secret_key = 'any random string'

host = 'http://127.0.0.1:5000/s/' #Change this to the URL you are using.

@app.route('/', methods=['GET','POST'])
def index():
	if 'username' not in session:
		#flash("Please login to continue")
		return redirect(url_for('login'))
	form = ShortenForm()
	if form.validate_on_submit():
		if(form.short_link.data):
			short_link = form.short_link.data
		else:
			short_link = ''.join(random.choices(string.ascii_letters + string.digits, k=5))

		long_link = form.link.data
		
		while(not is_short_link_valid(short_link)):
			short_link = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
		if not (long_link.startswith("http://") or long_link.startswith("https://")):
			long_link = 'http://'+long_link
		owner = session['id']
		if add_link(short_link, long_link, owner):
			# return jsonify(short_link = short_link)
			short_link = host+short_link
			# print("Short Link:"+short_link)
			return render_template('result.html', short_link=short_link)
		else:
			return '<h1>Server Error</h1>', 500

	return render_template('index.html',form=form)

@app.route('/s/<short_link>/', methods=['GET'])
def resolve(short_link):
	increment_count(short_link)
	long_link = get_link(short_link)
	if(long_link is not None):
		return redirect(long_link, code=302)
	else:
		return render_template('404.html')

@app.route('/checkAvailable',methods=['GET'])
def checkAvailabe():
	sl = request.args.get('link')
	if(sl and len(sl)>4 and len(sl)<11):
		if(is_short_link_valid(sl)):
			msg = {"available":"true"}
		else:
			msg = {"available":"false"}
	else:
		msg = {"available":"false"}

	return jsonify(msg)

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	print(form.validate_on_submit())
	if form.validate_on_submit():
		username = form.name.data
		password = form.password.data
		password1 = form.password_conf.data
		if password != password1:
			return '<h1>Password do not match!</h1>'
		if check_user_present(username):
			flash('User already present')
			return redirect(url_for('login'))
		hashed_pwd = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
		if bcrypt.checkpw(password.encode('utf8'), hashed_pwd):
			res = create_user(username, hashed_pwd)
			username,_,user_id = login_user(username)
		if res:
			session['id'] = user_id
			session['username'] = username
			flash('Signup Success!')
			return redirect(url_for('index'))
		else:
			flash('Signup Failed!')
			return redirect(url_for('signup'))

	return render_template('signup.html',form=form)

@app.route('/analysis/', methods=['GET'])
def analysis():
	if 'username' not in session:
		flash("Please login to continue")
		return redirect(url_for('login'))
	user_id = session['id']
	res = get_analysis(user_id)
	print(res)
	return render_template('analysis.html', res=res, host=host)


@app.route('/login/', methods=['GET', 'POST'])
def login():
		form = LoginForm()
		if form.validate_on_submit():
			username = form.name.data
			password = form.password.data
			user_name, user_pwd_hash, user_id = login_user(username)
			if user_name is None:
				flash('User not present')
				return redirect(url_for('login'))
			elif not bcrypt.checkpw(password.encode('utf8'), user_pwd_hash):
				flash('Incorrect Password!')
				return redirect(url_for('login'))
			else:
				session['id'] = user_id
				session['username'] = username
				#flash('Login Success!')
			return redirect(url_for('index'))
			
		return render_template('login.html',form=form)


@app.route('/logout/', methods=['GET'])
def logout():
	session.pop('username', None)
	session.pop('id', None)
	return redirect(url_for('login'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.png')

@app.route('/static/<filename>')
def send(filename):
	return send_from_directory(os.path.join(app.root_path, 'static'), filename);

@app.route('/delete/<short_link>')
def delete(short_link):
	if delete_link(short_link):
		flash('Link Deleted')
	else:
		flash("Delete failed")
	return redirect(url_for('analysis'))

@app.route('/activateToggle',methods=['GET'])
def activateToggle():
	short_link = request.args.get('sl')
	status = request.args.get('status')
	flag, new_status = activeToggle(short_link, status)
	if(new_status and flag):
		return jsonify({"status":1,"new_status":new_status})
	else:
		return jsonify({"status":0,"new_status":new_status})

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
