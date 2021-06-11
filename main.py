from dbmanager import *

if __name__ == '__main__':
    while True:
        print('Welcome to Pass Manager ! Choose an option :\n1.Register an new user\n2.Login to an existing account\n3.Exit')
        print()
        option = int(input())
        p_db = PasswordDB()

        if option == 1:
            p_db.register_user()

        elif option == 2:
            p_db.login()

        elif option == 3:
            print('Thank You !')
            p_db.exit()
            sys.exit()

        if p_db.logged_in:
            name = p_db.name
            u_db = UserPasswordDB(name)
            print('Welcome back, {}'.format(p_db.name))
            print()
            while p_db.logged_in:
                print('What would you like to do :\n1.Register a new Password\n2.Get Password for a url\n3.Show all registered passwords\n4.Logout')
                print()
                user_option = int(input())

                if user_option == 1:
                    u_db.register_password()

                elif user_option == 2:
                    u_db.show_password()

                elif user_option == 3:
                    u_db.show_all()

                elif user_option == 4:
                    break
