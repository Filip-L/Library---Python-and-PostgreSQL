import db
import functions


#!!!If you want to log in as admin -> login: admin, password: admin!!!
def start():
    """Function to start program"""
    db.check_db_exist()
    print("Hello in Library.")
    while True:
        choose = functions.menu_options()
        if choose == 4:
            break
        functions.chosen_option(choose)

start()
