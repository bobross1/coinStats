import requests
import re
from bs4 import BeautifulSoup

def telegram_scraper(url):
    """Function retrieves members and online members data of telegram channel.
    
    Parameters
    ----------
    url: str
        Telegram url to scrape
    Returns
    -------
    members: int
        Number of members in telegram group
    online members:
        Number of members currenlty online
    """
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }

    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    members, online = soup.find("div", class_="tgme_page_extra").string.replace(" ", "").split(",")
    members = re.match(r'\d+', members).group()
    online = re.match(r'\d+', online).group()
    return members, online