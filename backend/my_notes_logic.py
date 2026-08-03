from datetime import datetime, timedelta
import sqlite3
from backend.db_setup import DB_PATH

# FETCHING ALL NOTES FROM DB
def get_all_notes():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # access columns by name, like a dict
    cursor = conn.cursor()

    # SQL QUERY
    cursor.execute("SELECT * FROM note WHERE is_deleted = 0 ORDER BY created_at DESC")

    rows = cursor.fetchall()
    conn.close()

    # CONVERT DATA FROM DB (rows) TO PLAIN DICTS ({"id", "title", etc})
    return [dict(row) for row in rows]

# ADDING NOTES TO THE DB
def add_note(note_name, note_text, note_type):
    raw_tmstmp_now = datetime.now()
    tmstmp_now = raw_tmstmp_now.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("insert into note (note_name,note_text, note_type, modified_at) values (?,?,?,?)",(note_name,note_text, note_type, tmstmp_now ))
    conn.commit()
    conn.close()

# UPDATING NOTES FROM DB
def update_note(note_id, note_name, note_text):
    raw_tmstmp_now = datetime.now()
    tmstmp_now = raw_tmstmp_now.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("update note set note_name = ?, note_text = ?, modified_at = ? where note_id = ?",(note_name,note_text,tmstmp_now, note_id))
    conn.commit()
    conn.close()

# DELETING NOTES FROM MY_NOTES, SENDING TO TRASH BIN
def delete_note(note_id):
    raw_tmstmp_now = datetime.now()
    tmstmp_now = raw_tmstmp_now.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("update note set is_deleted = 1, modified_at = ?, deleted_at = ? where note_id = ?",(tmstmp_now, tmstmp_now, note_id))
    conn.commit()
    conn.close()