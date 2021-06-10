import sqlite3
import sys
from tabulate import tabulate
from getpass import getpass 
import os

THIS_FILE_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(THIS_FILE_PATH)
PWD_DIR = os.path.join(BASE_DIR,'Passwords_DB')

os.makedirs(PWD_DIR,exist_ok=True)

class PasswordDB():

    conn = sqlite3.connect('passwords_db')
    c = conn.cursor()
    logged_in = False

    #def __init__(self,name,pwd):
    #    self.name = name
    #    self.pwd = pwd
    
    def update_database(self):
        query = 'INSERT INTO users ("username","password") VALUES ("{}","{}")'.format(self.name,self.pwd)
        self.c.execute(query)
        self.conn.commit()

    def register_user(self):
        self.name = input('Enter Username :')
        self.pwd = getpass('Enter Password :')
        self.pwd2 = getpass('Confirm Password :')
        print()
        if self.pwd == self.pwd2:
            query = 'SELECT 1 FROM users WHERE username="{}"'.format(self.name)
            self.c.execute(query)
            user_is_present = self.c.fetchall()
            if len(user_is_present) == 0:
                self.update_database()
                print('User Created succesffully !')
                print()
                go_to_login = input('Proceed to login : Y/N\n(N will take you back to the home page)...')
                print()
                if go_to_login.lower() == 'y':
                    self.login()
                elif go_to_login.lower() == 'n':
                    pass
            else:
                print('Inavlid Username, please use a different username')
                print()
                self.register_user()
        else:
            print('Passwords do not match')
            self.register_user()

    def login(self):
        self.name = input('Enter your Username :')
        self.pwd = getpass('Enter your Password :')
        print()
        query = 'SELECT 1 FROM users WHERE username="{}" AND password="{}"'.format(self.name,self.pwd)
        self.c.execute(query)
        user_is_present = self.c.fetchall()
        if len(user_is_present) != 0:
            self.logged_in = True
        else :
            print('Invalid Username or password...')
            print()
            self.login()

    def exit(self):
        self.conn.close()

class UserPasswordDB(PasswordDB):

    def __init__(self,name):
        self.name = name
        self.conn = sqlite3.connect('{}/{}_db'.format(PWD_DIR,self.name))
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS passwords (website TEXT PRIMARY KEY,password TEXT NOT NULL)')
        self.conn.commit()

    def register_password(self):
        url = input('Enter URL of Website :')
        pwd = getpass('Enter password for {} :'.format(url))
        print()
        query = 'INSERT INTO passwords (website,password) VALUES ("{}","{}")'.format(url,pwd)
        self.c.execute(query)
        print('SUCCESS')
        print()
        self.conn.commit()
        #self.conn.close()

    def show_password(self):
        url = input('Enter URL to find :')
        print()
        query = 'SELECT password from passwords WHERE (website="{}")'.format(url)
        self.c.execute(query)
        pwd = self.c.fetchone()
        if pwd == None:
            print('No data found, did you enter URL correctly ?')
            print()
        else:
            for i in pwd:
                print (i)
            print()

    def show_all(self):
        query = 'SELECT * from passwords'
        self.c.execute(query)
        table = self.c.fetchall()
        if len(table) == 0:
            print('No results to display')
            print()
        else:
            print(tabulate(table,headers=['Website Name','Password']))
            print()
            #for t in table:
            #    print('Website name - {}\nPassword - {}'.format(t[0],t[1]))
            #    print('*'*26)
            #    print()
