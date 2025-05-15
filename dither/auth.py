import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from mysql.connector.errors import IntegrityError

from dither.db import database

bp = Blueprint('auth', __name__, url_prefix='/auth')

hasher = PasswordHasher()


@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		with database() as db:
			with db.cursor() as cur:
				try:
					cur.execute('INSERT INTO Users (username, password_hash) VALUES (%s, %s)', (username, hasher.hash(password)))
				except IntegrityError:
					flash('Username "%s" already exists!')
					return redirect(url_for('auth.register'))
				db.commit()
				session['username'] = username
			return redirect('/homepage')
	return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		with database() as db:
			with db.cursor() as cur:
				cur.execute('SELECT password_hash FROM Users WHERE username = %s LIMIT 1', [username])
				result = cur.fetchone()
				try:
					hash = str(result[0])
					hasher.verify(hash, password)
				except:
					flash('Invalid username or password!')
					return redirect(url_for('auth.login'))

				session['username'] = username
				return redirect('/homepage')
	return render_template('auth/login.html')
