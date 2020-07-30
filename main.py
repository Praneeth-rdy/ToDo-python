import os
import sqlite3
import database, users, gui

# Options while user is logged out
def select_option_lo(connection, existing_users):

    print('You are not signed in!')

    # printing existing_users
    users.print_users(existing_users)

    # Asking user for an option
    print('Select any of the following options:')
    option = input('1) {}\n2) {}\n3) {}\n4) {}\n'.format('SignIn', 'SignUp', 'RemoveUser', 'quit'))
    if option == '1':
        users.sign_in(connection, existing_users)
    elif option == '2':
        users.sign_up(connection, existing_users)
    elif option == '3':
        users.remove_user(connection, existing_users)
    elif option == '4':
        return
    else:
        print('Invalid option chosen! Please retry!\n')
        select_option_lo(connection, existing_users)

# Options while user is logged in
def select_option_li(connection, existing_users):

    current_user = users.logged_in_user(connection)

    # Print the currently logged in username
    print('You are currently logged in as {}'.format(current_user))

    # Asking user for an option
    print('Select any of the following options:')
    option = input('1) {}\n2) {}\n3) {}\n'.format('Continue', 'SignOut', 'quit'))

    if option == '1':
        # Passing current user and user's tasks as arguments
        gui.display(connection, current_user, database.get_tasks(connection, current_user))
    elif option == '2':
        users.sign_out(connection, existing_users)
    elif option == '3':
        return
    else:
        print('Invalid option chosen! Please retry!\n')
        select_option_li(connection, existing_users)



if __name__ == "__main__":
    # Database initialization for first time use of app.
    database.first_initialize()

    # Creating a connection to the database
    connection = sqlite3.connect('./db/todo.sqlite3')
    c = connection.cursor()

    # List of existing_users
    existing_users = [row for row in c.execute('SELECT * FROM users')]

    if users.logged_in_user(connection) == None:
        if len(existing_users) == 0:
            users.print_users(existing_users)
            users.sign_up(connection, existing_users)
        else:
            select_option_lo(connection, existing_users)
    else:
        select_option_li(connection, existing_users)
    
    connection.commit()
    connection.close()
