# from os import PRIO_PROCESS
from db import create_connection
from telegram_scraper import telegram_scraper
from cmc import get_latest_coin_data
from pathlib import Path
import datetime
import time
import random
import os

def update_symbols_data():
    dir_path = Path('coinStats/data/database.db').absolute()
    conn = create_connection(dir_path) # productie
    # conn = create_connection('data/database.db') # local
    cur = conn.cursor()
    symbols_data = cur.execute("SELECT id, cmc_id, telegram_url FROM coins").fetchall()
    cmc_ids = [elem[1] for elem in symbols_data]
    latest_cmc_data = get_latest_coin_data(cmc_ids)
    try:
        for id, cmc_id, telegram_url in symbols_data:
            price = latest_cmc_data[cmc_id]['price']
            mcap = latest_cmc_data[cmc_id]['mcap']
            percent_change_1h = latest_cmc_data[cmc_id]['percent_change_1h']
            cmc_rank = latest_cmc_data[cmc_id]['cmc_rank']
            telegram_members, telegram_members_online = telegram_scraper(telegram_url)
            
            # push to database
            cur.execute("INSERT INTO data(coin_id, date, users, online, marketcap, price, cmcrank, percent_change_1h)\
                         VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (id, datetime.datetime.now().strftime("%D %H:%M"),
                         telegram_members, telegram_members_online, mcap, price, cmc_rank, percent_change_1h))
            time.sleep(random.randrange(0,2))
            conn.commit()
        
        cur.close()
        log("Succes")
    except Exception as e:
        print(e)

def log(message):
    dir_path = Path('coinStats/update_data.py').parent.absolute()
    full_path = os.path.join(dir_path / "scraper_log.txt")
    log = open(full_path, "a")
    log.write("\n")
    log.write(datetime.datetime.now().strftime("%D %H:%M"))
    log.write(" ")
    log.write(message)
    log.close()

if __name__ == '__main__':
    try:
        update_symbols_data()
    except Exception as e:
        log(e)