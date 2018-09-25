#!/usr/bin/python3
from scraper import Scraper
from configparser import ConfigParser


def main():
    config = ConfigParser()
    config.read('config')
    db_host = config['Database']['Host']
    db_port = int(config['Database']['Port'])
    db_name = config['Database']['Name']
    db_collection = config['Database']['Collection']

    url = config['Scrape']['Url']

    scraper = Scraper(url)
    # 3211594
    scraper.start(3211594)


if __name__ == '__main__':
    main()
