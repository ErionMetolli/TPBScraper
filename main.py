#!/usr/bin/python3
import sys

from scraper import Scraper
from configparser import ConfigParser
from database import Database

config = ConfigParser()
config.read('config')
db_host = config['Database']['Host']
db_port = int(config['Database']['Port'])
db_username = config['Database']['Username']
db_password = config['Database']['Password']
db_name = config['Database']['Name']
db_collection = config['Database']['Collection']
url = config['Scrape']['Url']


def main():
    scraper = Scraper(url)
    # 3211594
    scraper.start(3211594)


def export_to_db():
    database = Database(db_host, db_port, db_username, db_password, db_name, db_collection)

    database.export_data()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'export':
        export_to_db()
    else:
        main()
