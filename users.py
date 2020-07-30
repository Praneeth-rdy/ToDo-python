import main

def remove_user(connection, existing_users):
    username = input('Enter the username to be removed: ')
    if username in [user[1] for user in existing_users]:
        connection.cursor().execute('DELETE FROM users WHERE name = ?', (username,))
        connection.commit()
        existing_users = [row for row in connection.cursor().execute('SELECT * FROM users')]
        print('User {} removed!\n'.format(username))
        main.select_option_lo(connection, existing_users)
    else:
        print('User not found! Please retry!\n')
        main.select_option_lo(connection, existing_users)

# Prints all existing users
def print_users(existing_users):
    if len(existing_users) == 0:
        print('No existing users found!')
    else:
        print('Existing users are:')
        for user_tuple in existing_users:
            print('{} {}'.format('=>', user_tuple[1]))

# Returns username if loggedin else None
def logged_in_user(connection):
    c = connection.cursor()
    is_logged_in = c.execute("SELECT value FROM variables WHERE name = ? ", ('is_logged_in',)).fetchall()[0][0]
    if is_logged_in == 'False':
        return None
    else:
        return c.execute("SELECT value FROM variables WHERE name = ? ", ('logged_in_user',)).fetchall()[0][0]

def sign_up(connection, existing_users):
    new_user = input('Please enter a username to create a user:\n')
    if new_user not in [user[1] for user in existing_users]:
        existing_users.append((len(existing_users)+1, new_user, 'None'))
        connection.cursor().execute('INSERT INTO users(name, tasks) VALUES(?,?)', (new_user, 'None'))
        connection.commit()
        print("User sign up successful! Now try 'signing in' using the registered username.\n")
        main.select_option_lo(connection, existing_users)
    else:
        print('User already exists! Try using a different username.\n')
        main.select_option_lo(connection, existing_users)

def sign_in(connection, existing_users):
    current_user = input('Enter your registered username to sign in: ')
    if current_user in [user[1] for user in existing_users]:
        c = connection.cursor()
        c.execute("UPDATE variables SET value = 'True' WHERE name = 'is_logged_in'")
        c.execute("UPDATE variables SET value = ? WHERE name = 'logged_in_user'", (current_user,))
        connection.commit()
        print('User sign in successful!\n')
        main.select_option_li(connection, existing_users)
    else:
        print('User not found! Please retry!\n')
        main.select_option_lo(connection, existing_users)

def sign_out(connection, existing_users):
    c = connection.cursor()
    c.execute("UPDATE variables SET value = 'False' WHERE name = 'is_logged_in'")
    c.execute("UPDATE variables SET value = 'None' WHERE name = 'logged_in_user'")
    connection.commit()
    print('User sign out successful!\n')
    main.select_option_lo(connection, existing_users)





'''data = [('praneeth1',),('praneeth2',), ('praneeth3',), ('praneeth4',)]
c.executemany('INSERT INTO users(name) VALUES(?)', data)
connection.commit()'''