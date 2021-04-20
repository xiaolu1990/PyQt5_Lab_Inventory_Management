# ################################################################
# File name:    database_mech.py
# Author:       Zhangshun Lu
# Create on:    2021-04-20
# Description:  Backend module for managing the mechanics database
# ################################################################

import sqlite3
from sqlite3 import Error
import pandas as pd


def create_table_mech():
    # Connect to a database
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS mechanics (
                                Description text,
                                PartNo text,
                                Category text,
                                Cabinet text,
                                Amount text,
                                Notes text     
                )""")

    # Commit command
    conn.commit()
    # Close connection
    conn.close()


def add_row(description="", part_number="", category="", cabinet="", amount="", notes=""):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("INSERT INTO mechanics VALUES (?, ?, ?, ?, ?, ?)",
              (description, part_number, category, cabinet, amount, notes))
    conn.commit()
    conn.close()


def add_rows(information):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.executemany(
        "INSERT INTO mechanics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", information)
    conn.commit()
    conn.close()


def search_row(id=""):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    if not id:
        id = "some words"
    try:
        c.execute("SELECT rowid, * from mechanics WHERE rowid=?", (id,))
    except Error as e:
        print(e)
    row = c.fetchone()
    conn.commit()
    conn.close()
    return row


def search_rows(description="", part_number="", category="", cabinet="", amount="", notes=""):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()

    if not description:
        description = "some words"
    if not part_number:
        part_number = "some words"
    if not category:
        category = "some words"
    if not cabinet:
        cabinet = "some words"
    if not amount:
        amount = "some words"
    if not notes:
        notes = "some words"

    try:
        c.execute("""SELECT rowid, * FROM mechanics WHERE 
                    Description=? OR PartNo=? OR Category=? OR
                    Cabinet=? OR Amount=? OR Notes=?""",
                  (description, part_number, category, cabinet, amount, notes))
        rows = c.fetchall()
        conn.commit()
        conn.close()
        return rows

    except Error as e:
        print(e)
    conn.commit()
    conn.close()


def delete_row(id=""):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    if not id:
        id = "some words"
    c.execute("DELETE FROM mechanics WHERE rowid=?", (id,))
    conn.commit()
    conn.close()


def update_row(id="", description="", part_number="", category="", cabinet="", amount="", notes=""):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("""UPDATE mechanics SET Description=?, PartNo=?, Category=?, Cabinet=?, Amount=?, Notes=? WHERE rowid=?""",
              (description, part_number, category, cabinet, amount, notes, int(id)))
    conn.commit()
    conn.close()


def show_table():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM mechanics")
    rows = c.fetchall()
    c.close()
    conn.commit()
    conn.close()
    return rows


def to_csv():
    conn = sqlite3.connect("inventory.db", detect_types=sqlite3.PARSE_COLNAMES)
    db_df = pd.read_sql_query("SELECT * FROM mechanics", conn)
    db_df.to_csv('mechanics_inventory.csv', index=False)


def main():
    pass


if __name__ == "__main__":
    main()
