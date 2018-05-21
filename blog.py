from flask import Flask ,render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
from datetime import datetime
import pymongo
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google
from werkzeug.contrib.fixers import ProxyFix

client = MongoClient('mongodb://sky-bot:GOLDENdiamond10@ds147228.mlab.com:47228/pblog')

app = Flask(__name__)
app.config['SECRET_KEY'] = '1354854kugsd6f4sd6f6sd4fs6d4fsdf'

app.wsgi_app = ProxyFix(app.wsgi_app)

app.config['MONGO_DB'] = 'pblog'
app.config['MONGO_URI'] = 'mongodb://sky-bot:GOLDENdiamond10@ds147228.mlab.com:47228/pblog'

mongo = PyMongo(app)

github_blueprint = make_github_blueprint(client_id='9d419b34bdbaee8511e1', client_secret='72ec523170e7947d8725e19a430318d49af67ac6')
google_blueprint = make_google_blueprint(client_id="1025163688283-gttkllr7rvbq80mrmnl6lf4l5kq8nds7.apps.googleusercontent.com",client_secret="m6crZtQAw6DBgzw3A_xbWF_I",scope=["profile", "email"])

app.register_blueprint(github_blueprint, url_prefix= '/github_login')
app.register_blueprint(google_blueprint, url_prefix="/google_login")

@app.route('/github')
def github_login():
	if not github.authorized:
		return redirect(url_for('github.login'))

	account_info = github.get('/user')

	if account_info.ok:
		print("----------------------")
		account_info_json = account_info.json()
		return '<h1>Your Github name is {}'.format(account_info_json['login'])

	return '<h1>Request Failed</h1>'

@app.route("/google")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    return "You are {email} on Google".format(email=resp.json()["email"])


@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/')
def index():
	db = client['user']
	user = mongo.db.user
	# user = user.find()
	user = user.find().sort('post_id', pymongo.ASCENDING)
	return render_template('index.html', user= user)


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/post/<int:p_id>', methods=['POST','GET'])
def post(p_id):
	db = client['user'] 
	user = mongo.db.user
	user1 = user.find_one({'post_id': p_id})
	claps = int(user1['claps'])
	print("------------")
	print(claps)
	if request.method == 'POST':
		if request.form['submit'] == 'claps':
			claps = claps + 1
			user1['claps'] = str(claps)
			user.save(user1)

	print(claps)
	return render_template('post.html',user = user1)


@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/add')
def add():	
	return render_template('add.html')

@app.route('/addpost', methods=['POST','GET'])
def addpost():
	db = client['user'] 
	user = mongo.db.user
	post_id = user.count()

	print(request.form['title'])

	claps = "0"
	user.insert({'post_id': post_id, 'title': request.form['title'], 'subtitle':request.form['subtitle'], 'author': request.form['author'],
	 'blogcontent': request.form['blogcontent'],'datetime': datetime.now(),'claps' : claps})
			
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug=True)