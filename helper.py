import pandas as pd
import logging
from sqlite3 import Error

def read_coins_txt():
    with open('coins.txt', 'r') as f:
        lines = f.readlines()
        coins = lines[0].strip().replace(" ", "").split(",")
    f.close()
    #TODO: make list unique
    return coins

def get_coin_name(conn, symbol):
    cur = conn.cursor()
    cur.execute(f"SELECT name FROM coins WHERE symbol=\"{symbol}\";")
    return cur.fetchone()[0]

def telegram_data_coin(conn, coin):
    """ select all telegram members data from coin and return in a dataframe
    :param conn: Connection object
    :param coin: Coin name 
    :returns: dataframe with date as index and data
    """
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT id FROM coins WHERE symbol=\"{coin}\";")
        coin_id = cur.fetchone()[0]
        query = f"SELECT * FROM data WHERE coin_id=\"{coin_id}\";"
        cur.execute(query)
        rows = cur.fetchall()
        df_membercount = pd.DataFrame({'index': [x[2] for x in rows], 
                        'data': [float(x[3]) for x in rows]})
        df_onlinecount = pd.DataFrame({'index': [x[2] for x in rows], 
                        'data': [float(x[4]) for x in rows]}) 
        return df_membercount.set_index('index'), df_onlinecount.set_index('index')
    
    except Error as e:
        logging.error(e, exc_info=True)

def price_data_coin(conn, coin):
    """ select all telegram members data from coin and return in a dataframe
    :param conn: Connection object
    :param coin: Coin name 
    :returns: dataframe with date as index and data
    """
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT id FROM coins WHERE symbol=\"{coin}\";")
        coin_id = cur.fetchone()[0]
        query = f"SELECT marketcap, price, cmcrank, percent_change_1h FROM data WHERE coin_id=\"{coin_id}\";"
        results = cur.execute(query).fetchone()
        marketcap, price, cmc_rank, percent_change_1h = results[0], results[1], results[2], results[3]
        return price, marketcap, cmc_rank, percent_change_1h
    
    except Error as e:
        logging.error(e, exc_info=True)