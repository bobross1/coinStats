from scrapers.telegram_scraper import scrape_telegram_data
from helpers.cmc import get_latest_symbols_data
from helpers.db import sql_create_data_table, sql_create_symbols_table, create_table
from pathlib import Path
import datetime
import time
import random
import os
import sqlite3
from sqlite3 import Error


def update_symbols_data():
    """ Retrieve and push new data to the database. """
    # local
    # dir_path = Path('coinStats/data/database.db').absolute()
    conn = sqlite3.connect('data/database.db')
    if conn is not None:
        # create tables
        create_table(conn, sql_create_symbols_table)
        create_table(conn, sql_create_data_table)
    else:
        print('Something wrong with database')

    # prod
    # dir_path = Path('/root/coinStats/data/database.db').absolute()
    # conn = sqlite3.connect(dir_path)
    
    cur = conn.cursor()
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
#        log("Succes")
    except Exception as e:
        print(e)
#       log(e)

def log(message):
    """ Logger for cronjobs. """
    dir_path = Path('coinStats/update_data.py').parent.absolute()
    full_path = os.path.join(dir_path / "scraper_log.txt")
    log = open(full_path, "a")
    log.write("\n")
    log.write(datetime.datetime.now().strftime("%D %H:%M"))
    log.write(" ")
    log.write(message)
    log.close()

if __name__ == '__main__':
    update_symbols_data()