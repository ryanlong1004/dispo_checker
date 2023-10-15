"""Responsible for Sqlite3 database interactions"""
import sqlite3
from typing import Any


def get_db_connection(name):
    """returns connection to db file"""
    return sqlite3.connect(name)


def create_table(cursor: sqlite3.Cursor):
    """creates the table if it doesn't exist"""
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
    """inserts item into database"""
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
            item.strain,
        ],
    )


def find_best_available(
    cursor: sqlite3.Cursor, ignored_categories=[]
) -> dict[str, Any]:
    """returns the best available product, ignore ignored_categories"""
    result = cursor.execute(
        f"""select * from items where category not in ({to_string_list(ignored_categories)}) ORDER BY timestamp DESC, price ASC, thc_percentage DESC;"""
    )
    return dict(zip(column_names(cursor), result.fetchone()))


def column_names(cursor):
    """returns the column names from a query"""
    keys = [description[0] for description in cursor.description]
    return keys


def to_string_list(ignored_categories):
    """converts a list of names to a format for sql IN/NOT IN"""
    ignored_categories = ", ".join([(f'"{x}"') for x in ignored_categories])
    return ignored_categories
