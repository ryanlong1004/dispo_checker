import sqlite3


def get_db_connection(name):
    return sqlite3.connect(name)


def create_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
CREATE TABLE IF NOT EXISTS items (
id integer primary key autoincrement,
name string,
price float,
thc_percentage float,
weight float,
brandname string,
quantity_available integer,
category string, 
strain string,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""
    )


def insert_item(cursor: sqlite3.Cursor, item):
    cursor.execute(
        """INSERT INTO items(name, price, thc_percentage, weight, brandname, quantity_available, category, strain) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
        [
            item.name,
            item.price,
            item.thc_percentage,
            item.weight,
            item.brandname,
            item.quantity_available,
            item.category,
            item.strain
        ],
    )
    
def find_best_available(cursor: sqlite3.Cursor):
    result = cursor.execute("""select * from items where category not in ('hash', 'sugar', 'rso', 'diamonds', 'applicators') ORDER BY timestamp DESC, price ASC, thc_percentage DESC;""")
    return result.fetchone()