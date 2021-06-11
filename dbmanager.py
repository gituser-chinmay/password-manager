import io
import sqlite3
import sys
from tabulate import tabulate
from getpass import getpass 
import os
from cryptography.fernet import Fernet
from tempfile import TemporaryFile

#These assignments are used to define directories-
THIS_FILE_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(THIS_FILE_PATH)
PWD_DIR = os.path.join(BASE_DIR,'Passwords_DB')
KEY_DIR = os.path.join(BASE_DIR,'User_keys')

os.makedirs(PWD_DIR,exist_ok=True)
os.makedirs(KEY_DIR,exist_ok=True)

class PasswordDB():

    conn = sqlite3.connect('passwords_db') #Create connection to database
    c = conn.cursor() #Create cursor for the database
    logged_in = False

    def update_database(self):
        self.generateKey()
        with open ('{}/{}key.key'.format(KEY_DIR,self.name),'wb') as f:
            key=f.write(self.key) #The key for the user must be read from the User_keys directory

        query = 'INSERT INTO users ("username","password","key") VALUES ("{}","{}","{}")'.format(self.name,self.pwd,key)
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
            if len(user_is_present) == 0: #To check if any data was retrieved, 0 means there is no user with the username given so it is safe to use it
                self.update_database()
                print('User Created succesffully !')
                print()
                go_to_login = input('Proceed to login : Y/N\n(N will take you back to the home page)...')
                print()
                if go_to_login.lower() == 'y':
                    self.login()
                elif go_to_login.lower() == 'n':
                    pass #The loop in the main.py takes care of this situation
            else:
                print('Inavlid Username, please use a different username')
                print()
                self.register_user() #Recursion has been used to call this function again incase any requirements have not been met
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
        if len(user_is_present) != 0: #Check if there is a user present with the username and password
            self.logged_in = True
        else :
            print('Invalid Username or password...')
            print()
            self.login()

    def generateKey(self):
        self.key = Fernet.generate_key()

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
        password = self._encrypt(pwd)
        print()
        query = 'INSERT INTO passwords (website,password) VALUES ("{}","{}")'.format(url,password)
        self.c.execute(query)
        print('SUCCESS')
        print()
        self.conn.commit()
    
    def _encrypt(self,pwd):
        with open ('{}/{}key.key'.format(KEY_DIR,self.name),'rb') as f:
            key=f.read()
        self.cipher_suite = Fernet(key) #Instantiates an object of Fernet class with key as an initialising parameter
        bytes_password = bytes((pwd),'utf-8') #Encrypt method of Fernet takes bytes input, therefore it is necessary to convert the password into bytes format
        enc_pwd = self.cipher_suite.encrypt(bytes_password)
        return enc_pwd.decode()

    def show_password(self):
        with open ('{}/{}key.key'.format(KEY_DIR,self.name),'rb') as f:
            key=f.read()
        self.cipher_suite = Fernet(key)
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
                enc_pwd = i.encode() #The encrypted password is stored as text in the database, it has to be converted to bytes for operations.
                decrypted_password = self.cipher_suite.decrypt(enc_pwd)
                print (decrypted_password.decode()) #Bytes type data is converted back into string to allow user to see their password
            print()

    def show_all(self):
        table = []
        with open ('{}/{}key.key'.format(KEY_DIR,self.name),'rb') as f:
            key=f.read()
        self.cipher_suite = Fernet(key)
        query = 'SELECT * from passwords'
        self.c.execute(query)
        data = self.c.fetchall()
        if len(data) == 0:
            print('No results to display')
            print()
        else:
            for d in data:
                enc_pwd = d[1].encode() 
                decrypted_password = self.cipher_suite.decrypt(enc_pwd)
                table.append((d[0],decrypted_password)) #Here, the passwords are stored in encrypted form on the database, but the user doesn't need to see that.
                #Therefore when this method is called, all the passwords in the table are decrypted and the list table is appended with tuples containing (website name, password)
                #This list will be used by the tabulate module

            print(tabulate(table,headers=['Website Name','Password']))
            print()
