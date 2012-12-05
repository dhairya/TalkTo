from __future__ import with_statement
from contextlib import closing
# all the imports
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


# configuration
DATABASE = '/Users/dhairyadand/Documents/HandsOn/Software/Flask/talkto/talkto.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# @app.before_request
# def before_request():
# 	g.db = connect_db()

# @app.teardown_request
# def teardown_request(exception):
# 	g.db.close()

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()


def connect_db():
	return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	if hasattr(g, 'db'):
		g.db.close()

def get_connection():
	db = getattr(g, '_db', None)
	if db is None:
		db = g._db = connect_db()
	return db

@app.route('/')
def what():
	db = get_connection()
	cur = db.execute('select name, office, what from entries order by id desc')
	entries = [dict(name=row[0], office=row[1], what=row[2]) for row in cur.fetchall()]
	return render_template('what.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
	db = get_connection()
	db.execute('insert into entries (name, office, what) values (?, ?, ?)', [request.form['yourname'], request.form['office'], request.form['what']])
	db.commit()
	return redirect(url_for('what'))

if __name__ == '__main__':
	#init_db()
	app.run()