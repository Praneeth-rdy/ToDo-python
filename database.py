import os
import sqlite3

def first_initialize():
    # Creating a directory(db) for databases if not exists
    if not os.path.exists('db'):
        os.mkdir('db')
    if not os.path.exists('./db/todo.sqlite3'): # Initializing the database for the first time use
        
        # Creating the database
        connection = sqlite3.connect('./db/todo.sqlite3')
        c = connection.cursor()
        
        # Creating table to store user data
        c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, tasks TEXT)')
        
        # Creating table to store static variables
        c.execute('CREATE TABLE IF NOT EXISTS variables(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, value TEXT)')

        # Creating variables for logged_in_user and is_logged_in.
        # Logged out => is_logged_in = False and logged_in_user = None
        data = [('is_logged_in', 'False'), ('logged_in_user', 'None')]
        c.executemany('INSERT INTO variables(name, value) VALUES(?,?)', data)

        # Commiting changes and closing database connection
        connection.commit()
        connection.close()

# Pushing tasks of user to connected database
def push_task(connection, username, task):
    c = connection.cursor()
    old_tasks = get_tasks(connection, username)
    if old_tasks == None:
        updated_tasks = task
    else:
        updated_tasks = old_tasks + ',' + task
    c.execute("UPDATE users SET tasks = ? WHERE name = ? ", (updated_tasks, username))
    connection.commit()
# Getting tasks of user from connected database
def get_tasks(connection, username):
    c = connection.cursor()
    tasks = c.execute('SELECT tasks FROM users WHERE name = ?', (username,)).fetchall()[0][0]
    if tasks == 'None':
        return None
    else:
        return tasks