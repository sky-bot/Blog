from flask import Flask ,render_template, request, redirect, url_for, jsonify
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



@app.route('/')
def index():
	db = client['user']
	user = mongo.db.user
	# user = user.find()
	print(type(user))
	print("---------------")
	user = user.find().sort('_id', pymongo.DESCENDING)
	page = int(request.args.get('page', 2))
#	page = request.args.get(get_page_parameter(), type=int, default=1)
	per_page = 1
	offset = (page-1) * per_page
	q = request.args.get('q')
	search = False
	if q:
		search = True
	
	pagination = Pagination(page=page,per_page=per_page, offset=offset, total=user.count(), search=search, record_name='user')
	return render_template('index.html', user= user, pagination = pagination)


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