import sqlite3
import threading

# Create tables in their respective databases
def setup_databases():
    users_conn = sqlite3.connect("users.db")
    orders_conn = sqlite3.connect("orders.db")
    products_conn = sqlite3.connect("products.db")

    # Users Table
    users_conn.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    # Orders Table
    orders_conn.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER
        )
    """)
    # Products Table
    products_conn.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL
        )
    """)
    
    users_conn.commit()
    orders_conn.commit()
    products_conn.commit()
    
    users_conn.close()
    orders_conn.close()
    products_conn.close()

# Insert data into tables
def insert_users():
    users_data = [
        (1, 'Alice', 'alice@example.com'),
        (2, 'Bob', 'bob@example.com'),
        (3, 'Charlie', 'charlie@example.com'),
        (4, 'David', 'david@example.com'),
        (5, 'Eve', 'eve@example.com'),
        (6, 'Frank', 'frank@example.com'),
        (7, 'Grace', 'grace@example.com'),
        (8, 'Alice', 'alice@example.com'),
        (9, 'Henry', 'henry@example.com'),
        (10, None, 'jane@example.com')
    ]
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    for user in users_data:
        try:
            cursor.execute("INSERT INTO Users (id, name, email) VALUES (?, ?, ?)", user)
        except sqlite3.IntegrityError as e:
            print(f"Error inserting user {user}: {e}")
    conn.commit()
    conn.close()

def insert_products():
    products_data = [
        (1, 'Laptop', 1000.00),
        (2, 'Smartphone', 700.00),
        (3, 'Headphones', 150.00),
        (4, 'Monitor', 300.00),
        (5, 'Keyboard', 50.00),
        (6, 'Mouse', 30.00),
        (7, 'Laptop', 1000.00),
        (8, 'Smartwatch', 250.00),
        (9, 'Gaming Chair', 500.00),
        (10, 'Earbuds', -50.00)
    ]
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    for product in products_data:
        try:
            cursor.execute("INSERT INTO Products (id, name, price) VALUES (?, ?, ?)", product)
        except sqlite3.IntegrityError as e:
            print(f"Error inserting product {product}: {e}")
    conn.commit()
    conn.close()

def insert_orders():
    orders_data = [
        (1, 1, 1, 2),
        (2, 2, 2, 1),
        (3, 3, 3, 5),
        (4, 4, 4, 1),
        (5, 5, 5, 3),
        (6, 6, 6, 4),
        (7, 7, 7, 2),
        (8, 8, 8, 0),
        (9, 9, 1, -1),
        (10, 10, 11, 2)
    ]
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    for order in orders_data:
        try:
            cursor.execute("INSERT INTO Orders (id, user_id, product_id, quantity) VALUES (?, ?, ?, ?)", order)
        except sqlite3.IntegrityError as e:
            print(f"Error inserting order {order}: {e}")
    conn.commit()
    conn.close()

# Main function to run threads
def main():
    setup_databases()
    threads = [
        threading.Thread(target=insert_users),
        threading.Thread(target=insert_products),
        threading.Thread(target=insert_orders)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("Data inserted successfully.")

# View database content
def view_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {db_name.split('.')[0].capitalize()}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

if __name__ == "__main__":
    main()
    # Uncomment below lines to view specific databases
#view_database("users.db")
#view_database("products.db")
#view_database("orders.db")

