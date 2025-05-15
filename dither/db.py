from contextlib import contextmanager

import mysql
import click
from flask import g, current_app

DB_USER = 'root'
DB_PASS = 'letmein'
DB_HOST = 'mysql'


def get_database_connection():
	if 'db' not in g:
		g.db = mysql.connector.connect(
			user=DB_USER, password=DB_PASS,
			database='dither',
			host=DB_HOST, buffered=True)
		g.db.commit()
	return g.db


def close_database_connection(e=None):
	db = g.pop('db', None)
	if db is not None:
		db.close()


@contextmanager
def database():
	db = get_database_connection()
	try:
		yield db
	finally:
		close_database_connection()


@contextmanager
def cursor():
	with database() as db:
		with db.cursor() as cur:
			try:
				yield cur
			except:
				pass


def initialize_database():
	with cursor() as cur:
		with current_app.open_resource('schema-oneline.sql') as file:
			for line in file.readlines():
				cur.execute(line)


def clear_database():
	with cursor() as cur:
		cur.execute('DROP TABLE IF EXISTS dither')


@click.command('reset-db')
def reset_db_command():
	clear_database()
	initialize_database()
	click.echo('Reset the database.')


@click.command('init-db')
def init_db_command():
	initialize_database()
	click.echo('Initialized the database.')


def init_app(app):
	app.teardown_appcontext(close_database_connection)
	app.cli.add_command(reset_db_command)
	app.cli.add_command(init_db_command)
