from datetime import datetime, timedelta
import sqlite3
from backend.db_setup import DB_PATH

# FETCHING ALL NOTES FROM TRASHED_NOTE TABLE
def get_all_trashed_notes():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # access columns by name, like a dict
    cursor = conn.cursor()

    # SQL QUERY
    cursor.execute("SELECT * FROM note where is_deleted = 1 ORDER BY modified_at DESC")

    rows = cursor.fetchall()
    conn.close()

    # CONVERT DATA FROM DB (rows) TO PLAIN DICTS ({"id", "title", etc})
    return [dict(row) for row in rows]

# RESTORING NOTES TO THE NOTE TABLE
def restore_note(note_id):
    raw_tmstmp_now = datetime.now()
    tmstmp_now = raw_tmstmp_now.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("update note set is_deleted = 0, modified_at = ? where note_id = ?",(tmstmp_now, note_id))
    conn.commit()
    conn.close()

# DELETING NOTES FROM DB (upon clicking the button)
def permanently_delete_note(note_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("delete from note where note_id = ?",(note_id,))
    conn.commit()
    conn.close()

# DELETING NOTES FROM DB AFTER 30 DAYS
def auto_delete_note():
    cutoff = datetime.now() - timedelta(days=30)
    cutoff_str = cutoff.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("delete from note where deleted_at < ?", (cutoff_str,))
    conn.commit()
    conn.close()

