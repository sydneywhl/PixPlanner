import sqlite3
from db_setup import DB_PATH

# ADD TEST NOTES IN NOTE TABLE
def dev_add_test_notes(): #my_notes
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    test_notes = [
        ("Grocery List", "Milk, eggs, bread, coffee", "sticky_note"),
        ("Project Ideas", "Build a to-do app, learn SQLite, redesign portfolio", "sticky_note"),
        ("Meeting Notes", "Discuss Q3 roadmap with the team", "note_page"),
        ("Random Thoughts", "Maybe I should get a plant for my desk", "note_page"),
    ]

    cursor.executemany("INSERT INTO note(note_name, note_text, note_type) VALUES (?, ?, ?)", test_notes)

    conn.commit()
    conn.close()

    print(f"Seeded {len(test_notes)} test notes.")

# CLEAR ALL TEST NOTES + RESET AUTO INCREMENT IN NOTE TABLE
def dev_clear_all_test_notes(): #my_notes
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM note")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'note'")
    conn.commit()
    conn.close()

# CLEAR USERS IN THE USERS TABLE
def dev_clear_user():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'users'")
    conn.commit()
    conn.close()

# ADD TRASHED_NOTES IN TRASHED_NOTE TABLE
def dev_add_trashed_notes(): #trash_bin
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    test_notes = [
        ("Grocery List", "Milk, eggs, bread, coffee", "sticky_note", 1),
        ("Project Ideas", "Build a to-do app, learn SQLite, redesign portfolio", "sticky_note", 1),
        ("Meeting Notes", "Discuss Q3 roadmap with the team", "note_page", 1),
        ("Random Thoughts", "Maybe I should get a plant for my desk", "note_page",1),
    ]

    cursor.executemany("INSERT INTO note(note_name, note_text, note_type, is_deleted) VALUES (?, ?, ?, ?)", test_notes)

    conn.commit()
    conn.close()

    print(f"Seeded {len(test_notes)} test trash notes.")

# CLEAR ALL TRASHED NOTES + RESET AUTO INCREMENT
def dev_clear_all_trashed_notes(): #my_notes
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trashed_note")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'trashed_note'")
    conn.commit()
    conn.close()

def dev_remove_unique():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA index_list('note')")
    #cursor.execute("ALTER table note drop index note_pk")
    conn.commit()
    conn.close()

if __name__ == "__main__":

    # ADD NOTES AT MY_NOTES
    #dev_add_test_notes()

    # CLEAR NOTES AT MY_NOTES
    #dev_clear_all_test_notes()
    #print(f"Deleted test notes and resetted auto increment.")

    # CLEAR USERS
    #dev_clear_user()
    #print("Deleted users.")

    # ADD NOTES AT TRASHED_NOTE
    #dev_add_trashed_notes()

    # CLEAR NOTES AT TRASHED_NOTE
    #dev_clear_all_trashed_notes()

    # REMOVE UNIQUE
    print(dev_remove_unique())
