import sqlite3
from sqlite3 import Error
import logging
from helpers.cmc import get_symbol_cmc_data, get_latest_symbols_data
from scrapers.telegram_scraper import scrape_telegram_data
from update_data import update_symbols_data, log
from pathlib import Path
import time
import random
import datetime

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
    """ Add all symbols to the database for the first time"""
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
    """ Function to fill the new database for the first time """
    cur = conn.cursor()
    db_contains_data = cur.execute("SELECT * FROM data").fetchone()
    if not db_contains_data:
        # update all symbols first time
        symbols_data = cur.execute("SELECT id, cmc_id, telegram_url FROM symbols").fetchall()
        cmc_ids = [elem[1] for elem in symbols_data]
        latest_cmc_data = get_latest_symbols_data(cmc_ids)
        try:
            for id, cmc_id, telegram_url in symbols_data:
                price = latest_cmc_data[cmc_id]['price']
                mcap = latest_cmc_data[cmc_id]['mcap']
                percent_change_1h = latest_cmc_data[cmc_id]['percent_change_1h']
                cmc_rank = latest_cmc_data[cmc_id]['cmc_rank']
                telegram_members, telegram_members_online = scrape_telegram_data(telegram_url)
                
                # push to database
                cur.execute("INSERT INTO data(coin_id, date, telegram_members, telegram_members_online, marketcap, price,\
                                        cmcrank, percent_change_1h) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",\
                                        (id, datetime.datetime.now().strftime("%D %H:%M"),
                                        telegram_members, telegram_members_online, mcap, price, cmc_rank, percent_change_1h))
                time.sleep(random.randrange(0,2))
                conn.commit()
            cur.close()
        except Exception as e:
            print(e)

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