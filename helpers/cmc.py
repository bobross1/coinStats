from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import re


def do_request(url, parameters, api_key):
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': f'{api_key}',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e

def get_symbol_cmc_data(symbol):
    """ Extract all required data from the cmc api based on coin symbol.
        :param symbol: coin symbol to query data from
        :returns: cmc_id (int), website url (string), symbol name (string), telegram url (string)
    """
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info' 
    all_data = do_request(url, parameters = {'symbol': symbol})
    cmc_id = int(all_data["data"][symbol]['id'])
    website_url = str(all_data["data"][symbol]['urls']['website'][0])
    symbol_name = str(all_data["data"][symbol]['name'])
    coin_chat_urls = all_data["data"][symbol]['urls']['chat']
    # get telegram url
    r = re.compile("https://t.me/")
    telegram_url = str(list(filter(r.match, coin_chat_urls))[0])
    return cmc_id, website_url, symbol_name, telegram_url

def get_latest_symbols_data(cmc_ids):
    """ Get latest data for all symbols in database.
        :param cmc_ids: coin market cap ids of each symbol
        :returns: dictionary with all cmc_ids and its data 
    """
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    all_data = do_request(url, parameters={'id': ','.join([str(elem) for elem in cmc_ids])})
    d = {}
    for cmc_id in cmc_ids:
        price = float(all_data["data"][f"{cmc_id}"]["quote"]["USD"]["price"]) 
        mcap = float(all_data["data"][f"{cmc_id}"]["quote"]["USD"]["market_cap"])
        percent_change_1h = float(all_data["data"][f"{cmc_id}"]["quote"]["USD"]["percent_change_1h"])
        cmc_rank = int(all_data["data"][f"{cmc_id}"]["cmc_rank"])
        d[cmc_id] = {'price': price,
                     'mcap': mcap,
                     'percent_change_1h': percent_change_1h,
                     'cmc_rank': cmc_rank}
    return d

    
    

