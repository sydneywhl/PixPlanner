# backend/db_setup.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pix_planner.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #USER
    cursor.execute("""
        create table if not exists users (
            user_id integer primary key autoincrement,
            user_name text not null unique,
            user_password_hash text not null
        )
    """)

    # NOTE GROUP: GROUPS STICKY NOTES INTO STICKY PAD AND NOTE PAGE INTO NOTE BOOKS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS note_group(
            note_group_id integer PRIMARY KEY AUTOINCREMENT,
            note_group_name text not null,
            note_group_type text not null,
            note_group_categories text,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_at TIMESTAMP DEFAULT NULL,
            is_deleted integer not null,
            deleted_at TIMESTAMP DEFAULT NULL
        )
    """)

    # NOTE TABLE: STORES STICKY NOTE AND NOTE PAGE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS note (
            note_id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_name TEXT NOT NULL,
            note_text TEXT,
            note_type TEXT,
            note_categories TEXT,
            remind_at TIMESTAMP DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_at TIMESTAMP DEFAULT NULL,
            is_deleted integer not null,
            deleted_at TIMESTAMP DEFAULT NULL,
            note_group_id integer,
            
            foreign key(note_group_id) references note_group(note_group_id)
        )
    """)

    # TRASHED_NOTE GROUP: GROUPS STICKY NOTES INTO STICKY PAD AND NOTE PAGE INTO NOTE BOOKS
    #cursor.execute("""
    #    CREATE TABLE IF NOT EXISTS trashed_note_group(
    #        note_group_id integer PRIMARY KEY AUTOINCREMENT,
    #        note_group_type text not null,
    #       note_group_name text not null,
    #        note_group_categories text,
    #        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    #        modified_at TIMESTAMP DEFAULT NULL
    #    )
    #""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings(
            setting_id integer PRIMARY KEY AUTOINCREMENT,
            setting_key text not null,
            setting_value text not null,
            user_id integer,
            foreign key(user_id) references users(user_id)
        )
    """)

    #cursor.execute("""
        #CREATE TABLE IF NOT EXISTS remind_note(
        #)
    #""")


    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized.")
