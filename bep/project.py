from flask import Flask, render_template, request, redirect
from flask import url_for, flash, jsonify

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Book, User
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
	open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Book Exchange Program"

# Create session and connect to DB
engine = create_engine('sqlite:///library.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create a state token to prevent request forgery.
# Store it in the session for later validation.
@app.route('/login')
def showLogin():
	state = (''.join(random.choice(string.ascii_uppercase + string.digits)
		for x in xrange(32)))
	login_session['state'] = state
	return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
	# Validate state token
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Obtain authorization code
	code = request.data
	try:
		# Upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets(
			'client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(
			json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Check that the access token is valid.
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?'
		'access_token=%s' % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	# If there was an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
	# Verify that the access token is used for the intended use
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(
			json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Verify that the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		response = make_response(
			json.dumps(
				"Token's client ID does not match app's."), 401)
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response
	# Check to see if user is already logged in
	stored_credentials = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps(
			'Current user is already connected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Store the access token in the session for later use.
	login_session['credentials'] = credentials
	login_session['gplus_id'] = gplus_id
	# Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)
	data = answer.json()
	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']
	# Add provider to login session.
	login_session['provider'] = 'google'
	# See if user exists, if it doesn't make a new one
	user_id = getUserID(data["email"])
	if not user_id:
		user_id = createUser(login_session)
	login_session['user_id'] = user_id
	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += ' "style = "width: 300px; height: 300px; border-radius:'
	output += ' 150px;-webkit-border-radius: 150px;-moz-border-radius:'
	output += ' 150px;"> '
	flash("you are now logged in as %s" % login_session['username'])
	print "done!"
	return output


# User Helper Functions
def createUser(login_session):
	newUser = User(name=login_session['username'],
		email=login_session['email'],
		picture=login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(
		email=login_session['email']).one()
	return user.id


def getUserInfo(user_id):
	user = session.query(User).filter_by(id=user_id).one()
	return user


def getUserID(email):
	try:
		user = session.query(User).filter_by(email=email).one()
		return user.id
	except:
		return None


# Disconnet: Revoke a current user's token & reset their login_session.
@app.route('/gdisconnect')
def gdisconnect():
	# Only disconnect a connected user.
	credentials = login_session.get('credentials')
	if credentials is None:
		response = make_response(
			json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	access_token = credentials.access_token
	url = 'https://accounts.google.com/o/oauth2/'
	url += 'revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]
	if result['status'] != '200':
		# For whatever reason, the given token was invalid.
		response = make_response(
			json.dumps('Failed to revoke token for given user.', 400))
		response.headers['Content-Type'] = 'application/json'
		return response


# JSON APIs to view a genre's book list information.
@app.route('/genre/<int:genre_id>/book/JSON/')
def genreBooksJSON(genre_id):
	items = session.query(Book).filter_by(genre_id=genre_id).all()
	return jsonify(Books=[i.serialize for i in items])


# JSON APIs to view a book's information.
@app.route('/genre/<int:genre_id>/book/<int:book_id>/JSON/')
def BookJSON(genre_id, book_id):
	bookItem = session.query(Book).filter_by(id=book_id).one()
	return jsonify(Book=bookItem.serialize)


# JSON APIs to view genre list.
@app.route('/genre/JSON/')
def genresJSON():
	genres = session.query(Genre).all()
	return jsonify(genres=[r.serialize for r in genres])


# Show all genres.
@app.route('/')
@app.route('/genre/')
def showGenres():
	genres = session.query(Genre).order_by(asc(Genre.name))
	if 'username' not in login_session:
		return render_template('publicgenres.html', genres=genres)
	else:
		return render_template('genres.html', genres=genres)
		print "show user genres"


# Create a new genre.
@app.route('/genre/new/', methods=['GET', 'POST'])
def newGenre():
	if 'username' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		newGenre = Genre(name=request.form['name'],
			user_id=login_session['user_id'])
		if not request.form['name'] or request.form['name'].isspace():
			flash('Name can not be empty!')
			return redirect(url_for('showGenres'))
		session.add(newGenre)
		flash('New Genre %s Successfully Created' % newGenre.name)
		session.commit()
		return redirect(url_for('showGenres'))
	else:
		return render_template('newGenre.html')


# Edit a genre.
@app.route('/genre/<int:genre_id>/edit/', methods=['GET', 'POST'])
def editGenre(genre_id):
	editedGenre = session.query(
		Genre).filter_by(id=genre_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if editedGenre.user_id != login_session['user_id']:
		ermsg = "<script>function myFunction() {alert('You are "
		ermsg += "not authorized to edit this genre. "
		ermsg += "Please create your own genre in order to edit.');}"
		ermsg += "</script><body onload='myFunction()''>"
		return ermsg
	if request.method == 'POST':
		if request.form['name'] and not request.form['name'].isspace():
			editedGenre.name = request.form['name']
			flash('Genre Successfully Edited %s' % editedGenre.name)
			return redirect(url_for('showGenres'))
		else:
			flash('Name can not be empty!')
			return redirect(url_for('showGenres'))
	else:
		return render_template('editGenre.html', genre=editedGenre)


# Delete a genre.
@app.route('/genre/<int:genre_id>/delete/', methods=['GET', 'POST'])
def deleteGenre(genre_id):
	genreToDelete = session.query(
		Genre).filter_by(id=genre_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if genreToDelete.user_id != login_session['user_id']:
		ermsg = "<script>function myFunction() {alert('You are "
		ermsg += "not authorized to delete this genre. "
		ermsg += "Please create your own genre in order to delete.');}"
		ermsg += "</script><body onload='myFunction()''>"
		return ermsg
	if request.method == 'POST':
		session.delete(genreToDelete)
		flash('%s Successfully Deleted' % genreToDelete.name)
		session.commit()
		return redirect(url_for('showGenres', genre_id=genre_id))
	else:
		return render_template('deleteGenre.html', genre=genreToDelete)


# Show a genre book.
@app.route('/genre/<int:genre_id>/')
@app.route('/genre/<int:genre_id>/book/')
def showBook(genre_id):
	genre = session.query(Genre).filter_by(id=genre_id).one()
	creator = getUserInfo(genre.user_id)
	items = session.query(Book).filter_by(
		genre_id=genre_id).all()
	if ('username' not in login_session or
	 creator.id != login_session['user_id']):
		return render_template('publicbook.html', items=items,
			genre=genre, creator=creator)
	else:
		return render_template('book.html', items=items, genre=genre,
			creator=creator)


# Create a new book item.
@app.route('/genre/<int:genre_id>/book/new/', methods=['GET', 'POST'])
def newBook(genre_id):
	if 'username' not in login_session:
		return redirect('/login')
	genre = session.query(Genre).filter_by(id=genre_id).one()
	if login_session['user_id'] != genre.user_id:
		ermsg = "<script>function myFunction() {alert('You are"
		ermsg += "not authorized to add book items to this genre. "
		ermsg += "Please create your own genre in order to add items."
		ermsg += "');}</script><body onload='myFunction()''>"
		return ermsg
	if request.method == 'POST':
		newItem = Book(name=request.form['name'],
			description=request.form['description'],
			price=request.form['price'],
			genre_id=genre_id,
			user_id=genre.user_id)
		if not request.form['name'] or request.form['name'].isspace():
			flash('Name can not be empty!')
			return redirect(url_for('showBook', genre_id=genre_id))
		session.add(newItem)
		session.commit()
		flash('New Book %s Item Successfully Created' % (newItem.name))
		return redirect(url_for('showBook', genre_id=genre_id))
	else:
		return render_template('newbook.html', genre_id=genre_id)


# Edit a book item.
@app.route('/genre/<int:genre_id>/book/<int:book_id>/edit',
	methods=['GET', 'POST'])
def editBook(genre_id, book_id):
	if 'username' not in login_session:
		return redirect('/login')
	editedItem = session.query(Book).filter_by(id=book_id).one()
	genre = session.query(Genre).filter_by(id=genre_id).one()
	if login_session['user_id'] != genre.user_id:
		ermsg = "<script>function myFunction() {alert('You are "
		ermsg += "not authorized to edit book items to this genre. "
		ermsg += "Please create your own genre in order to edit items."
		ermsg += "');}</script><body onload='myFunction()''>"
		return ermsg
	if request.method == 'POST':
		if request.form['name'] and not request.form['name'].isspace():
			editedItem.name = request.form['name']
		else:
			flash('Name can not be empty!')
			return redirect(url_for('showBook', genre_id=genre_id))
		if request.form['description']:
			editedItem.description = request.form['description']
		if request.form['price']:
			editedItem.price = request.form['price']
		session.add(editedItem)
		session.commit()
		flash('%s Successfully Edited' % (editedItem.name))
		return redirect(url_for('showBook', genre_id=genre_id))
	else:
		return render_template('editbook.html',
			genre_id=genre_id, book_id=book_id, item=editedItem)


# Delete a book item.
@app.route('/genre/<int:genre_id>/book/<int:book_id>/delete',
	methods=['GET', 'POST'])
def deleteBook(genre_id, book_id):
	if 'username' not in login_session:
		return redirect('/login')
	genre = session.query(Genre).filter_by(id=genre_id).one()
	itemToDelete = session.query(Book).filter_by(id=book_id).one()
	if login_session['user_id'] != genre.user_id:
		ermsg = "<script>function myFunction() {alert('You are "
		ermsg += "not authorized to delete book items to this genre. "
		ermsg += "Please create your own genre in order to delete items."
		ermsg += "');}</script><body onload='myFunction()''>"
		return ermsg
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash('%s Successfully Deleted' % (itemToDelete.name))
		return redirect(url_for('showBook', genre_id=genre_id))
	else:
		return render_template('deleteBook.html',
			genre_id=genre_id, item=itemToDelete)


# Disconnect based on provider in case there is more than one.
@app.route('/disconnect')
def disconnect():
	if 'provider' in login_session:
		if login_session['provider'] == 'google':
			gdisconnect()
			del login_session['gplus_id']
			del login_session['credentials']
#       if login_session['provider'] == 'facebook':
#           fbdisconnect()
#           del login_session['facebook_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']
		del login_session['user_id']
		del login_session['provider']
		flash("You have successfully been logged out.")
		return redirect(url_for('showGenres'))
	else:
		flash("You were not logged in")
		return redirect(url_for('showGenres'))


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
