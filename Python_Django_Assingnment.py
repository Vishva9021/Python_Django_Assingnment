import sqlite3
import threading
import random
import string

# Database file names
db_files = {
    "Users": "users.db",
    "Orders": "orders.db",
    "Products": "products.db"
}

# Create tables for each database
def initialize_database():
    for model, db_file in db_files.items():
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            if model == "Users":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL
                    )
                """)
            elif model == "Orders":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL
                    )
                """)
            elif model == "Products":
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        price REAL NOT NULL
                    )
                """)
            conn.commit()

# Insert data into the specified table
def insert_data(model):
    db_file = db_files[model]
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        for _ in range(10):  # Simulate 10 insertions
            if model == "Users":
                name = ''.join(random.choices(string.ascii_letters, k=8))
                email = f"{name.lower()}@example.com"
                cursor.execute("INSERT INTO Users (name, email) VALUES (?, ?)", (name, email))
            elif model == "Orders":
                user_id = random.randint(1, 10)
                product_id = random.randint(1, 10)
                cursor.execute("INSERT INTO Orders (user_id, product_id) VALUES (?, ?)", (user_id, product_id))
            elif model == "Products":
                name = ''.join(random.choices(string.ascii_letters, k=8))
                price = round(random.uniform(10, 100), 2)
                cursor.execute("INSERT INTO Products (name, price) VALUES (?, ?)", (name, price))
        conn.commit()

# Main function to simulate simultaneous insertions
def main():
    initialize_database()

    threads = []

    for model in db_files.keys():
        thread = threading.Thread(target=insert_data, args=(model,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Fetch and print results from each database
    for model, db_file in db_files.items():
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            print(f"Data in {model} database:")
            cursor.execute(f"SELECT * FROM {model}")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            print()

if __name__ == "__main__":
    main()
