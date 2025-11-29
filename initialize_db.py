import sqlite3
import os
import shutil 

DB_NAME = "face_database.db"

def execute_query(query, params=None, fetch=False):
    """Executes a query with optional parameters and fetches results if needed."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if fetch:
                return cursor.fetchall()

            conn.commit()
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def create_table():
    """Creates the users table if it doesn't exist and ensures images folder exists."""
    query = '''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            embedding BLOB NOT NULL
        )
    '''
    execute_query(query)
    print("✅ Table 'users' is ready.")

    # Create images folder if it doesn't exist
    if not os.path.exists("images"):
        os.makedirs("images")
        print("✅ 'images' folder created.")
    else:
        print("ℹ️ 'images' folder already exists.")

def insert_user(user_id, name, embedding):
    """Inserts a new user into the table."""
    query = "INSERT INTO users (user_id, name, embedding) VALUES (?, ?, ?)"
    execute_query(query, (user_id, name, sqlite3.Binary(embedding)))
    print(f" User '{name}' added successfully......!")

def show_users():
    """Displays all users in the database."""
    query = "SELECT user_id, name FROM users"
    users = execute_query(query, fetch=True)
    
    if users:
        print("\n Users in Database:")
        for user in users:
            print(f"ID: {user[0]} | Name: {user[1]}")
    else:
        print("\n⚠️ No users found in the database.")

def delete_user(user_id):
    """Deletes a user by user_id."""
    # Get user name first (required to delete folder)
    query = "SELECT name FROM users WHERE user_id = ?"
    result = execute_query(query, (int(user_id),), fetch=True)

    if not result:
        print("⚠️ User not found.")
        return

    name = result[0][0]

    # Delete from DB
    query = "DELETE FROM users WHERE user_id = ?"
    execute_query(query, (int(user_id),))
    print(f"✅ User ID {user_id} deleted.")

    # Now delete folder
    delete_user_folder(user_id, name)

def drop_table():
    """Drops the users table (CAUTION: Deletes all records)."""
    confirm = input("⚠️ Are you sure you want to delete the entire table? (yes/no): ").strip().lower()
    if confirm == "yes":
        execute_query("DROP TABLE IF EXISTS users")
        print(" Table 'users' deleted.")

        # NEW: Delete complete images/ folder
        if os.path.exists("images"):
            shutil.rmtree("images")
            print("🗑️ Deleted entire 'images' folder.")
        else:
            print("⚠️ No 'images' folder exists.")

    else:
        print(" Action canceled.")

def execute_custom_query():
    """Allows the DBA to enter a custom SQL query and executes it."""
    while True:
        query = input("\n📝 Enter your custom SQL query (or type 'exit' to cancel): ").strip()
        if not query:
            print("⚠️ Query cannot be empty. Please try again.")
            continue
        if query.lower() == "exit":
            print(" Custom query execution canceled.")
            return
        
        fetch_result = input("🔍 Do you expect a result set? (yes/no): ").strip().lower()
        fetch = fetch_result == "yes"

        result = execute_query(query, fetch=fetch)
        if fetch and result:
            print("\n📚 Query Results:")
            for row in result:
                print(row)
        print(" Query executed successfully....!")
        break

if __name__ == "__main__":
    while True:
        print("\n" + "="*30)
        print("..... Choose an option...")
        print("1️  Create Table")
        print("2️  Insert User")
        print("3️  Show Users")
        print("4️  Delete User")
        print("5️  Drop Table ⚠️ (Deletes All Data)")
        print("6️  Execute Custom Query")
        print("7️  Exit")
        print("="*30)

        choice = input("\nEnter choice (1-7): ").strip()
        
        if choice == "1":
            create_table()
        elif choice == "2":
            user_id = input("Enter User ID: ")
            name = input("Enter user name: ")
            embedding = input("Enter embedding data (as bytes): ").encode()  # Simulated binary data
            insert_user(user_id, name, embedding)
        elif choice == "3":
            show_users()
        elif choice == "4":
            user_id = input("Enter user ID to delete: ")
            delete_user(user_id)
        elif choice == "5":
            drop_table()
        elif choice == "6":
            execute_custom_query()
        elif choice == "7":
            print("👋 Exiting program.")
            break
        else:
            print("⚠️ Invalid choice. Please enter a valid option.")
