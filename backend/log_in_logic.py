import sqlite3

import bcrypt

from backend.db_setup import DB_PATH

# CHECKS IF THERE IS AN ACCOUNT MADE
def has_account_been_created():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) from users")
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

# IF USERS NEVER MADE AN ACCOUNT BEFORE
def create_one_account(username, password):
    try:
        password_hash = create_password_hash(password)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("insert into users (user_name, user_password_hash) values(?,?)", (username, password_hash))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# CHECKS IF THE USERNAME EXISTS
def username_exists(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("select count(*) from users where user_name = ?", (username,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

# VERIFIES THE LOGIN CREDENTIALS OF THE USER
def verify_login(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("select user_password_hash from users where user_name = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return False
    return bcrypt.checkpw(password.encode(),row[0].encode())

def create_password_hash(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()