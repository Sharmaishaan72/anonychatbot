import sqlite3
import datetime

class BotDatabase:
    def __init__(self, db_name="bot.db"):
        self.db_name = db_name
        self.con = sqlite3.connect(self.db_name, check_same_thread=False)
        self._setup()

    def _setup(self):
        """Create necessary tables if they don't exist."""
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    joindate DATE,
                    banned CHAR(1)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS marketing (
                    id INTEGER PRIMARY KEY,
                    joindate DATE,
                    messages INTEGER
                )
            """)  # Unused for now

    def fetch_users(self):
        """Fetch all users from the 'users' table."""
        cur = self.con.cursor()
        cur.execute("SELECT id FROM users")
        data = cur.fetchall()
        #print(data)
        return data

    def return_user_data(self, user_id: int):
        """Fetch a single user's data by ID."""
        cur = self.con.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cur.fetchone()

    def add_user(self, user_id: int):
        """Add a new user to the 'users' table."""
        with self.con:
            cur = self.con.cursor()
            cur.execute("""
                INSERT INTO users (id, joindate, banned) 
                VALUES (?, ?, ?)
            """, (user_id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "F"))
            print(f"User {user_id} added successfully.")
    
    def close(self):
        """Close the database connection."""
        self.con.close()
