import os
from pathlib import Path
import os

THIS_FILE_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(THIS_FILE_PATH)
PWD_DIR = os.path.join(BASE_DIR,'Passwords')

os.makedirs(PWD_DIR,exist_ok=True)

user = input('Name ?')
web = input('URL Domanin ?')
pwd = input('Password ?')

USER_PASSWORDS = os.path.join(PWD_DIR,'{}Passwords'.format(user))
os.makedirs(USER_PASSWORDS,exist_ok=True)

fname = ('passwords.txt')

password_file = os.path.join(USER_PASSWORDS,fname)

with open(password_file,'a') as f:
    f.write('Web - {}\nPassword - {}\n'.format(web,pwd) + '*'*26 + '\n') 