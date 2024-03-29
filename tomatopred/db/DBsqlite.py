
import sqlite3
import os

DATABASE = os.path.join(os.getcwd(),'tomatopred','data','data.db')
#c = co.cursor() 
def create_usertable():
	co = sqlite3.connect(DATABASE)
	c = co.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS userstable(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL,email TEXT NOT NULL UNIQUE,created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)')
	c.close()

def add_userdata(username,password,email):
	co = sqlite3.connect(DATABASE)
	c = co.cursor()
	c.execute('INSERT INTO userstable(username,password, email) VALUES (?,?,?)',(username,password,email))

	co.commit()
	c.close()

def login_user(username,password,email)->list:
	co = sqlite3.connect(DATABASE)
	c = co.cursor()
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ? AND email = ?',(username,password,email))
	data = c.fetchall()
	c.close()
	return data

def view_all_users():
	co = sqlite3.connect(DATABASE)
	c = co.cursor()
	c.execute('SELECT * FROM usertable')
	data = c.fetchall()
	c.close()
	return data

if __name__ == "__main__":
	create_usertable()

