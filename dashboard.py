import streamlit as st
import sqlite3
from helper import read_coins_txt, telegram_data_coin, price_data_coin, get_coin_name
from db import add_coins_db, create_connection, create_table , sql_create_coins_table, sql_create_data_table
# import plotly.express as px
import re

# connect to database
conn = create_connection('data/database.db')
if conn is not None:
    # create coins table
    create_table(conn, sql_create_coins_table)
    create_table(conn, sql_create_data_table)
    
    # fill first time
    #-----
else:
    print('Something wrong with database')

st.set_page_config(page_title="coinStats",
                    page_icon="📈",
                    layout="wide",
                    initial_sidebar_state="expanded")

# sidebar
st.sidebar.header("Menu2")
symbols = read_coins_txt()

# add coins to db (if not already in there)
if symbols == None:
    st.info("Add symbol(s) to the coins.txt file.")
else:
    add_coins_db(conn, symbols)
    

coin = st.sidebar.selectbox("Select coin:", symbols)
coin_name = get_coin_name(conn, coin)

# main page
st.title(f'{coin_name} ({coin})')

#load all data related to symbol
telegram_members, telegram_members_online = telegram_data_coin(conn, coin)
price, marketcap, cmc_rank, percent_change_1h = price_data_coin(conn, coin)


R1C1, R1C2, R1C3 = st.columns(3)
R1C1.metric("Ranking", f"# {cmc_rank}", "")
R1C2.metric("Marketcap", f"${round(marketcap,2)}", "")
R1C3.metric("Price", f"${round(price,2)}", f"{round(percent_change_1h,2)}% (1h)")
    
R2C1, R2C2 = st.columns(2)
with R2C1:
    st.text("Total telegram members")
    st.line_chart(telegram_members)

with R2C2:
    st.text("Telegram members online")
    st.line_chart(telegram_members_online)