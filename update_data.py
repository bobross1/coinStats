# from os import PRIO_PROCESS
from db import create_connection
from telegram_scraper import telegram_scraper
from cmc import get_latest_coin_data
from pathlib import Path
import datetime
import time
import random

def update_symbols_data():
#     dir_path = Path('coinStats/data/database.db').absolute()
#     print(dir_path)
    conn = create_connection('data/database.db')
    cur = conn.cursor()
    symbols_data = cur.execute("SELECT id, cmc_id, telegram_url FROM coins").fetchall()
    cmc_ids = [elem[1] for elem in symbols_data]
    latest_cmc_data = get_latest_coin_data(cmc_ids)
    try:
        for id, cmc_id, telegram_url in symbols_data:
            price = latest_cmc_data[str(cmc_id)]['price']
            mcap = latest_cmc_data[str(cmc_id)]['mcap']
            percent_change_1h = latest_cmc_data[str(cmc_id)]['percent_change_1h']
            cmc_rank = latest_cmc_data[str(cmc_id)]['cmc_rank']
            telegram_members, telegram_members_online = telegram_scraper(telegram_url)
            
            # push to database
            cur.execute("INSERT INTO data(coin_id, date, users, online, marketcap, price, cmcrank, percent_change_1h)\
                         VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (id, datetime.datetime.now().strftime("%D %H:%M"),
                         telegram_members, telegram_members_online, mcap, price, cmc_rank, percent_change_1h))
            time.sleep(random.randrange(0,2))
            
        cur.close()
        conn.commit()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    update_symbols_data()