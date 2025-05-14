import atexit
import traceback
from contextlib import contextmanager

import mysql
import mysql.connector
from flask import (
    Flask, flash, g, redirect, render_template, request, session, url_for, config
)

from argon2 import PasswordHasher

DB_USER = 'root'
DB_PASS = 'letmein'
DB_HOST = '127.0.0.1'

hasher = PasswordHasher()

app = Flask(__name__, template_folder='templates')
app.config.from_mapping(
	SECRET_KEY='dev'
)

@contextmanager
def database():
	if 'db' not in g:
		g.db = mysql.connector.connect(
			user=DB_USER, password=DB_PASS,
			database='Dither',
			host='mysql', buffered=True)

	try:
		yield g.db
	finally:
		db = g.pop('db', None)
		if db is not None:
			db.close()

@app.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		with database() as db:
			with db.cursor() as cur:
				cur.execute('INSERT INTO Users (username, password_hash) VALUES (%s, %s)', (username, hasher.hash(password)))
				db.commit()
				session['username'] = username
			return redirect('/homepage')
	return render_template('register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		with database() as db:
			with db.cursor() as cur:
				cur.execute('SELECT password_hash FROM Users WHERE username = %s LIMIT 1', [username])
				hash = str(cur.fetchone()[0])
				hasher.verify(hash, password)

				session['username'] = username
				return redirect('/homepage')
	return render_template('login.html')

def get_user_id(username, db):
	with db.cursor() as cur:
		cur.execute('SELECT user_id FROM Users WHERE username = %s', [username])
		return int(cur.fetchone()[0])

def get_followers(username, db):
	with db.cursor() as cur:
		cur.execute('SELECT COUNT(*) FROM Followers WHERE followee_id = %s', [get_user_id(username, db)])
		return int(cur.fetchone()[0])

@app.route('/makedb')
def makedb():
	with database() as db:
		with open('sql/schema.sql', 'r') as f:
			with db.cursor() as cur:
				cur.execute(f.read())
	return 'hi'

@app.route('/homepage')
def homepage():
	with database() as db:
		username = session.get('username')
		followers = get_followers(g.username, db)
		return render_template('homepage.html', **locals())

if __name__ == '__main__':
	app.run(debug=True)
