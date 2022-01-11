import sqlite3
from sqlite3 import Error
import logging
import re
from cmc import get_symbol_data

def create_connection(db_file):
    ''' create a database connection or create database (connect) '''
    try:
        return sqlite3.connect(db_file)
    except Error as e:
        logging.error(e, exc_info=True)

def create_table(conn, create_table_sql):
    """ create a table with create_table_sql argument
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def add_coins_db(conn, symbols):
    cur = conn.cursor()
    for symbol in symbols:
        exists = cur.execute(f"SELECT * FROM coins WHERE symbol = \"{symbol}\"").fetchall()
        if not exists:
            try:
                cmc_id, website_url, symbol_name,  telegram_url = get_symbol_data(symbol)
                cur.execute("INSERT INTO coins(cmc_id, name, symbol, telegram_url, website_url) VALUES(?, ?, ?, ?, ?)",
                (cmc_id, symbol_name, symbol, telegram_url, website_url))
                conn.commit()
            except Error as e:
                return f'Something went wrong: {e}'
        else:
            print('already in db')
    cur.close()

### queries for creating the database tables
sql_create_coins_table = """CREATE TABLE IF NOT EXISTS coins (
                                id integer PRIMARY KEY,
                                cmc_id integer NOT NULL,
                                name text NOT NULL,
                                symbol text NOT NULL,
                                telegram_url text NOT NULL,
                                website_url text NOT NULL
                            );"""

sql_create_data_table = """CREATE TABLE IF NOT EXISTS data (
                                id integer PRIMARY KEY,
                                coin_id integer NOT NULL,
                                date text NOT NULL,
                                users text NOT NULL,
                                online text NOT NULL,
                                marketcap real,
                                price real,
                                cmcrank int,
                                percent_change_1h real,
                                FOREIGN KEY (coin_id) REFERENCES coins (id)
                            );""" 