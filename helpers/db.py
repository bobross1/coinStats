import sqlite3
from sqlite3 import Error
import logging
from helpers.cmc import get_symbol_cmc_data
from tasks.update_data import update_symbols_data

def create_connection(db_file):
    """ Connect (or create) database """
    try:
        return sqlite3.connect(db_file)
    except Error as e:
        logging.error(e, exc_info=True)

def create_table(conn, create_table_sql):
    """ Create a table in db with create_table_sql argument
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def startup_db():
    """ Connect (or create) database """
    conn = create_connection('data/database.db')
    if conn is not None:
        # create tables
        create_table(conn, sql_create_symbols_table)
        create_table(conn, sql_create_data_table)
    else:
        print('Something wrong with database')
    return conn

def add_symbols_db(conn, symbols):
    cur = conn.cursor()
    for symbol in symbols:
        exists = cur.execute(f"SELECT * FROM symbols WHERE symbol = \"{symbol}\"").fetchall()
        if not exists:
            try:
                cmc_id, website_url, symbol_name,  telegram_url = get_symbol_cmc_data(symbol)
                cur.execute("INSERT INTO symbols(cmc_id, name, symbol, telegram_url, website_url) VALUES(?, ?, ?, ?, ?)",
                (cmc_id, symbol_name, symbol, telegram_url, website_url))
                conn.commit()
            except Error as e:
                return f'Something went wrong: {e}'
        else:
            print('already in db')
    cur.close()

def fill_db(conn):
    cur = conn.cursor()
    db_contains_data = cur.execute("SELECT * FROM data").fetchone()
    if not db_contains_data:
        update_symbols_data()

# Queries for creating the database tables
sql_create_symbols_table = """CREATE TABLE IF NOT EXISTS symbols (
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
                                telegram_members text,
                                telegram_members_online text,
                                marketcap real,
                                price real,
                                cmcrank int,
                                percent_change_1h real,
                                FOREIGN KEY (coin_id) REFERENCES symbols (id)
                            );""" 