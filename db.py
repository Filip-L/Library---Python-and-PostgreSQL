import psycopg2
import datetime


connection = None
cur = None


def connection_db():
    """Making connections with the database"""

    global connection, cur
    connection = psycopg2.connect(
        host="localhost",
        database="Library",
        user="postgres",
        password="admin",
        port=5432
    )
    connection.autocommit = True
    cur = connection.cursor()


def disconnect_db():
    """Closing connections with the database"""

    cur.close()
    connection.close()


def create_table_users():
    """The function of creating a table of users in the database"""

    connection_db()
    cur.execute("CREATE TABLE users(" 
                "user_id serial PRIMARY KEY,"
                "username VARCHAR (50) UNIQUE NOT NULL,"
                "password VARCHAR (50) NOT NULL"
                ");")
    disconnect_db()


def create_table_books():
    """The function of creating a table of books in the database"""    

    connection_db()
    cur.execute("CREATE TABLE books(" 
                "book_id serial PRIMARY KEY,"
                "title VARCHAR (100) UNIQUE NOT NULL,"
                "book_year INTEGER NOT NULL,"
                "author VARCHAR (100)"
                ");")
    disconnect_db()


def create_table_loan_history():
    """The function of create a table of loan history in the database"""   

    connection_db()
    cur.execute("CREATE TABLE loan_history(" 
                "loan_id serial PRIMARY KEY,"
                "book_id INTEGER NOT NULL,"
                "user_id INTEGER NOT NULL,"
                "loan_date DATE,"
                "loan_back_date DATE"
                ");")
    disconnect_db()


def create_admin_account():
    """Automatically create an administrator account"""

    connection_db()
    cur.execute("INSERT INTO users (username, password) VALUES('admin', 'admin')")
    disconnect_db()


def check_db_exist():
    """Trying to make all tables and admin account if they do not exist"""
    try:
        create_table_users()
    except psycopg2.errors.DuplicateTable:
        pass

    try:
        create_table_books()
    except psycopg2.errors.DuplicateTable:    
        pass

    try:
        create_table_loan_history()
    except psycopg2.errors.DuplicateTable:    
        pass

    try:
        create_admin_account()
    except psycopg2.errors.IntegrityError:
        pass


def create_user():
    """Function to create users and add to the user's table
    
    :params login: name of account
    :type login: str
    :params password: password to account
    :type password: str
    """

    while True:
        print("Creating account... or press ENTER to go back")
        login = input("Login: ")       
        if login == "":
            break
        connection_db()
        cur.execute("SELECT * FROM users WHERE username=(%s)", (login,))
        found_user = cur.fetchone()
        if found_user:
            print("This login already exist")
            continue

        password = input("Password: ")
        if len(password) < 3:
            print("Password must be longer than 3 characters")
            continue
        check_password = input("Repeat password: ")
        if password != check_password:
            print("Password are not the same")
            continue
        try:
            cur.execute("INSERT INTO users (username, password) VALUES(%s, %s)", (login, password))
        except psycopg2.errors.IntegrityError:
            print("This user already exist")
        disconnect_db()
        print("Success...")
        break


def add_book():
    """Function to create book and add to the user's table
    
    :params title: title of book
    :type title: str
    :params book_year: year of book
    :type book_year: int
    :params author: author of book
    :type author: str
    """
    while True:
        print("Adding book... or press ENTER to go back")
        title = input("Title: ").title()
        if not title:
            break
        try:
            book_year = int(input("Book year: "))  
        except ValueError:
            print("\nThe type must be int\n")
            continue
        author = input("Author: ")
        if not author:
            print("Author can not by empty") 
            continue
        connection_db()
        cur.execute("INSERT INTO books (title, book_year, author) VALUES(%s, %s, %s)", (title, book_year, author))
        disconnect_db()
        print("Success...")
        break


def show_users():
    """Funtction to show all users in the database"""

    connection_db()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    print(f"Number of users: {len(users)}")
    for user in users:
        print(f"ID: {user[0]}, Login: {user[1]}, {len(user[2]) * '*'}")
    disconnect_db()


def show_books():
    """Funtction to show all books in the database"""

    connection_db()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    print(f"Number of books: {len(books)}")
    for book in books:
        print(f"ID: {book[0]}, Title: {book[1]}, Year: {book[2]}, Author: {book[3]}")
    disconnect_db()


def log_in():
    """Function to log in on account
    
    :params login: name of account
    :type login: str
    :params password: password to account
    :type password: str
    :return login: if the password to account is correct
    :rertur True: if logging is successful
    :return False: if logging is unsuccessful
    :return None: if logging is unsuccessful
    :rtype login: str
    :rtype True, False: bool
    :rtype None: NoneType
    """

    while True:
        print("Logging... or press ENTER to go back")
        login = input("Login: ")
        if login == "":
            return False, None
        connection_db()
        cur.execute("SELECT * FROM users WHERE username=(%s)", (login,))
        found_user = cur.fetchone()
        disconnect_db()
        if not found_user:
            print("Wrong login")
            continue
        else:
            password = found_user[2]
            password_user = input("Password: ")
            if password == password_user:
                print("Success logging...")
                return True, login
            else:
                print("Wrong password.")
                continue


def search_book():
    """Function to looking for books and showing similar books if they exist
    
    :params searching_book: name of the book you are looking for
    :type searching_book: str
    """

    print("\nPress Enter if you want go back")
    while True:
        the_books_you_are_looking_for = []
        searching_book = input("Book name: ").title()
        if not searching_book:
            break       
        connection_db()
        cur.execute("SELECT * FROM books WHERE title ILIKE(%s);", (searching_book, ))
        found_book = cur.fetchall()
        cur.execute("SELECT * FROM books WHERE title ILIKE (%s);", ('%' + searching_book + '%', ))
        found_books = cur.fetchall()
        similar_found_books = [book for book in found_books]
        if not found_book:
            print("\nThis book is not in library, but you can find book with similar name.")
            if not found_books:
                print("\nThere is no books with similar name")
            else:
                print("\nBook with similar name:")
                for book in found_books:
                    print(f"Title: {book[1]}, Year: {book[2]}, Author: {book[3]}")            
        else:
            print("\nThe book you are looking for:")
            for book in found_book:
                the_books_you_are_looking_for.append(book)
                print(f"Title: {book[1]}, Year: {book[2]}, Author: {book[3]}")
            print("\nBook with similar name:")
            if set(similar_found_books) == set(the_books_you_are_looking_for) or not similar_found_books:
                print("There is no books with similar name")
            else:
                for book in found_books:
                    if book in the_books_you_are_looking_for:
                        pass
                    else:
                        if set(similar_found_books) == set(the_books_you_are_looking_for) or not similar_found_books:
                            print("There is no similar books")
                        else:
                            print(f"Title: {book[1]}, Year: {book[2]}, Author: {book[3]}")
        disconnect_db()
        print("\nSearch another book or press Enter to go back")


def show_your_books(login):
    """Function to show user books
    
    :params login: name of user
    :type login: str
    """

    print("Books which you have:")
    connection_db()
    cur.execute("SELECT user_id FROM users WHERE username = (%s)", (login,))
    user_id = cur.fetchone()
    cur.execute("SELECT b.title, b.book_year, h.loan_date FROM loan_history h JOIN books b ON h.book_id = b.book_id " \
                "JOIN users u ON h.user_id = u.user_id WHERE u.user_id = (%s) AND loan_back_date is NULL", (user_id,))
    user_books = cur.fetchall()
    if user_books:
        for book in user_books:
            print(f"{book[0]} {book[1]}, Loan date: {book[2]}")
    else:
        print("You do not have any book")
    disconnect_db()


def show_your_history(login):
    """Function to show user history
    
    :params login: name of user
    :type login: str
    """

    connection_db()
    cur.execute("SELECT user_id FROM users WHERE username = (%s)", (login,))
    user_id = cur.fetchone()
    cur.execute("SELECT b.title, b.book_year, h.loan_date, h.loan_back_date FROM books b JOIN loan_history h ON b.book_id = h.book_id " \
                "JOIN users u ON h.user_id = u.user_id WHERE u.user_id = (%s) AND loan_back_date is NOT NULL", (user_id,))
    user_old_books = cur.fetchall()
    print("Books which you had: ")
    if user_old_books:
        for book in user_old_books:
            print(f"{book[0]} {book[1]}, Loan date: {book[2]}, Date of returning: {book[3]}")
    else:
        print("You do not have any book in history")
    disconnect_db()


def delete_user():
    """Function to delete users of the database
    
    :params login: name of user
    :type login: str
    """
    while True:
        print("Deleting user... or press ENTER to go back")
        user = input("The user you want to delete: ")
        if user == 'admin':
            print("You can not delete admin account")
            continue
        if not user:
            break
        connection_db()
        cur.execute("SELECT * FROM users WHERE username = (%s)", (user,))
        check_user_exist = cur.fetchall()
        if not check_user_exist:
            print("This user do not exist")
            continue
        else:
            agreement = input("Press y if you sure or something else if you are not:").upper()
            if agreement == 'Y':
                cur.execute("DELETE FROM users WHERE username = (%s)", (user,))
                disconnect_db()
                print(f"User {user} deleted successfully")
                break
            else:
                continue
            

def delete_books():
    """Function to delete books of the database
    
    :params title: title of book
    :type title: str
    """

    while True:
        print("Deleting books... or press ENTER to go back")
        title = input("The book you want to delete: ").title()
        if not title:
            break
        connection_db()
        cur.execute("SELECT * FROM books WHERE title = (%s)", (title,))
        check_book_exist = cur.fetchall()
        if not check_book_exist:
            print("This book do not exist")
            continue
        else:
            agreement = input("Press y if you are sure or something else if you are not:")
            if agreement == 'y':
                cur.execute("DELETE FROM books WHERE title = (%s)", (title,))
                disconnect_db()
                print(f"Book {title} deleted successfully")
                break
            else:
                continue


def check_user_book():
    """Function to check user's book by admin
    
    :params user: user login
    :type user: str
    """
    while True:
        user = input("Which user you do want to check...  or press ENTER to go back: ")
        if not user:
            break
        connection_db()
        cur.execute("SELECT * FROM users WHERE username = (%s)", (user,))
        found_user = cur.fetchone()
        if not found_user:
            print("This user not exist, try again...")
            continue
        show_your_books(user)
        disconnect_db()
        continue


def borrow_book(login):
    """Function to let user's borrow book
    
    :params login: user who borrow a book
    :type login: str
    :params book_want_to_borrow: select book to borrow
    :type book_want_to_borrow: str
    :params confirm: confirm if you want to borrow book
    :type confirm: str
    """

    connection_db()
    cur.execute("SELECT * FROM users WHERE username = (%s)", (login,))
    user = cur.fetchone()
    user_id = int(user[0])
    while True:
        book_already_have = False
        book_want_to_borrow = input("Which book do you want to borrow... or press ENTER to go back: \n")
        book_want_to_borrow = book_want_to_borrow.title()
        if not book_want_to_borrow:
            break
        cur.execute("SELECT * FROM books WHERE title = (%s)", (book_want_to_borrow,))
        found_book_to_borrow = cur.fetchone()
        if not found_book_to_borrow:
            print("This book is not in library... Try again")
            continue
        cur.execute("SELECT b.title FROM loan_history h JOIN books b ON h.book_id = b.book_id " \
                    "JOIN users u ON h.user_id = u.user_id WHERE u.user_id = (%s) AND loan_back_date is NULL", (user_id,))
        your_books = cur.fetchall()
        for book in your_books:
            if book[0] == book_want_to_borrow:
                print("You have this book. Choose another book...")
                book_already_have = True
                break
        if book_already_have:
            continue
        confirm = input(f"Book {found_book_to_borrow[1]} {found_book_to_borrow[2]} is in library" \
                        " do you want to borrow this book? Press y if you are sure or ENTER to go back ")
        if not confirm == 'y':
            continue
        else:
            print(f"The book {found_book_to_borrow[1]} {found_book_to_borrow[2]} has been added to your loan list")
            cur.execute("INSERT INTO loan_history(book_id, user_id, loan_date, loan_back_date) " \
                        "VALUES (%s, %s, %s, %s)", (int(found_book_to_borrow[0]), user_id, datetime.date.today(), None))
            print("Success...")
            disconnect_db()
            break


def give_back_a_book(login):
    """Function to give back a book
    
    :params login: user who give back a book
    :type login: str
    :params book_to_give_back: book you want to give back
    :type book_to_give_back: str
    """

    while True:
        while True:
            check_user_books = []
            connection_db()
            cur.execute("SELECT user_id FROM users WHERE username = (%s)", (login,))
            user_id = cur.fetchone()
            cur.execute("SELECT b.title, b.book_year, h.loan_date FROM loan_history h JOIN books b ON h.book_id = b.book_id " \
                        "JOIN users u ON h.user_id = u.user_id WHERE u.user_id = (%s) AND loan_back_date is NULL", (user_id,))
            user_books = cur.fetchall()
            for i in range(len(user_books)):
                check_user_books.append(user_books[i-1][0])
            if not user_books:
                print("You do not have any book to give back")
                break
            else:
                print("Your books:\n")    
                for book in user_books:
                    print(f"{book[0]} {book[1]}, Loan date: {book[2]}")  
            break
        if not user_books:
            break
        while True:
            book_to_give_back = input("Which book do you want to give back... or press ENTER to go back \n").title()
            if not book_to_give_back:
                break
            if book_to_give_back not in check_user_books:
                print("You do not have this book")
                continue
            cur.execute("SELECT book_id FROM books WHERE title = (%s)", (book_to_give_back,))
            book_id = cur.fetchone()
            cur.execute("UPDATE loan_history SET loan_back_date = (%s) " \
                        "WHERE user_id = (%s) AND book_id = (%s) AND loan_back_date IS NULL", (datetime.date.today(), user_id, book_id))
            disconnect_db()
            print("Success...\n")
            continue
        break