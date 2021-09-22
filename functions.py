import db


def menu_options():
    """Function to show options
    Function show option what user can do in first step
    and take one argument from user
    
    :params choose: choosen number
    :type choose: int
    :return: chosen number
    :rtype: int
    """

    global choose
    choose = None
    print('\nWhat do you want to do?\n')
    while True:
        print('Choose: 1 if you want to make an account')
        print('Choose: 2 if you want to log in')
        print('Choose: 3 if you want to see the list of books')
        print("Choose: 4 if you want to exit")
        list_of_option = [1, 2, 3, 4]        
        try:
            choose = int(input("Choose... "))  
        except ValueError:
            print("\nThe type must be int.\n")
            continue

        if choose not in list_of_option:
            print("Choose number between 1 - 4")
            continue

        break
    return choose


def chosen_option(choose):
    """Function to take chosen number and start functions
    
    :param choose: number chosen by user
    :type choose: int
    """
    global login
    while True:
        if choose == 1:
            db.create_user()
            break

        if choose == 2:
            login_status, login = db.log_in()
            print(login_status)
            if login_status:
                if login == 'admin':
                    admin_menu()
                    break
                else:
                   user_menu()
                   break
            else:
                break
        if choose == 3:
            db.show_books()
            break


def user_menu():
    """Function to choose option in user options
    
    :params choose: choose a number
    :type book_to_give_back: int
    """
    print("\nWhat do you want to do?\n")
    while True:
        print('Choose: 1 if you want to search a book')
        print('Choose: 2 if you want show yours books')
        print('Choose: 3 if you want to borrow a book')
        print("Choose: 4 if you want to give back a book")
        print("Choose: 5 if you want to check your loan hisotry")
        print("Choose: 6 if you want to log out")
        list_of_option = [1, 2, 3, 4, 5, 6]
        try:
            login_choose = int(input("Choose... "))  
        except ValueError:
            print("\nChoose number between 1 - 5\n")
            continue
        if login_choose not in list_of_option:
            print("\nChoose number between 1 - 5\n")
            continue
        if login_choose == 1:
            db.search_book()
            continue
        if login_choose == 2:
            db.show_your_books(login)
            continue
        if login_choose == 3:
            db.borrow_book(login)
            continue
        if login_choose == 4:
            db.give_back_a_book(login)
            continue
        if login_choose == 5:
            db.show_your_history(login)
            continue
        if login_choose == 6:
            break

    

def admin_menu():
    """Function to choose option in admin options
    
    :params choose: choose a number
    :type book_to_give_back: int
    """

    print("What do you want to do?")
    while True:
        print('Choose: 1 if you want to add book')
        print('Choose: 2 if you want show users')
        print('Choose: 3 if you want to delete user')
        print("Choose: 4 if you want to show books")
        print('Choose: 5 if you want to delete books')
        print("Choose: 6 if you want to check user book")
        print("Choose: 7 if you want to log out")
        list_of_option = [1, 2, 3, 4, 5, 6, 7]
        try:
            choose = int(input("Choose... "))  
        except ValueError:
            print("\nThe type must be int\n")
            continue
        if choose not in list_of_option:
            print("Choose number between 1 - 7")
            continue
        if choose == 1:
            db.add_book()
            continue
        if choose == 2:
            db.show_users()
            continue
        if choose == 3:
            db.delete_user()
            continue
        if choose == 4:
            db.show_books()
            continue
        if choose == 5:
            db.delete_books()
            continue
        if choose == 6:
            db.check_user_book()
        if choose == 7:
            break
