# from tasks.update_data import log
from pathlib import Path
import datetime
import os

def log2(message):
    """ Logger for cronjobs. """
    dir_path = Path('coinStats/update_data.py').parent.absolute()
    full_path = os.path.join(dir_path / "scraper_log.txt")
    log = open(full_path, "a")
    log.write("\n")
    log.write(datetime.datetime.now().strftime("%D %H:%M"))
    log.write(" ")
    log.write(message)
    log.close()

if __name__ == "__main__":
    log2("test")