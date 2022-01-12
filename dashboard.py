import streamlit as st
from helper import read_symbols_txt, telegram_data_symbol, price_data_symbol, get_coin_name
from db import add_symbols_db, startup_db, fill_db, create_table, sql_create_data_table, sql_create_symbols_table, create_connection
from pathlib import Path

# Connect/create to database
conn = startup_db()

# dir_path = Path('coinStats/data/database.db').absolute()
# conn = create_connection(dir_path)
#local
# conn = create_connection('data/database.db')
if conn is not None:
    # create tables
    create_table(conn, sql_create_symbols_table)
    create_table(conn, sql_create_data_table)
else:
    print('Something wrong with database')

# Page settings
st.set_page_config(page_title="coinStats",
                    page_icon="📈",
                    layout="wide",
                    initial_sidebar_state="expanded")

# Sidebar
st.sidebar.header("Menu")
symbols = read_symbols_txt()

# Add coins to db (if not already in there)
if symbols == None:
    st.info("Add symbol(s) to the coins.txt file.")
else:
    # Fill db first time
    add_symbols_db(conn, symbols)
    fill_db(conn)
    
symbol = st.sidebar.selectbox("Select coin:", symbols)
coin_name = get_coin_name(conn, symbol)

# Main page
st.title(f'{coin_name} ({symbol})')

# Retrieve all data related to selected symbol
telegram_members, telegram_members_online = telegram_data_symbol(conn, symbol)
price, marketcap, cmc_rank, percent_change_1h = price_data_symbol(conn, symbol)

# Show data
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