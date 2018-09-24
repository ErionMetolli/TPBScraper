import string
import json
import socks
import socket
from pprint import pprint

def create_connection_fixed_dns_leak(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket
socket.create_connection = create_connection_fixed_dns_leak

from urllib import request
from urllib.error import HTTPError

from logger import Logger
from database  import Database

class Del:
    def __init__(self, keep=string.digits):
        self.comp = dict((ord(c),c) for c in keep)
    def __getitem__(self, k):
        return self.comp.get(k)

class Scraper:
    scraping = False

    def __init__(self, url, host, port, db_name, db_collection):
        self.url = url
        self.log = Logger(type(self).__name__).log
        self.DD = Del()
    
    def start(self, s):
        self.log('Starting scraping.')
        self.scraping = True
        count = s
        while True:
            req = request.Request(self.url + str(count))
            self.log('Current URL: ' + self.url + str(count))
            try:
                res = request.urlopen(req)
                html = res.read().decode('UTF-8')
                self.log('Fetched HTML.')

                magnet = html.split('href="magnet:?xt=urn:btih:')[1][:40]

                files_count = html.split('}); filelist = ')[1][:10]
                files_count = files_count.translate(self.DD)

                uploaded_date = '20' + html.split('<dd>20')[1][:21]

                seeders = html.split('<dt>Seeders:</dt>')[1].split('<dd>', 1)[1][:10]
                seeders = seeders.translate(self.DD)

                leechers = html.split('<dt>Leechers:</dt>')[1].split('<dd>', 1)[1][:10]
                leechers = leechers.translate(self.DD)

                comments = html.split('<dd><span id=\'NumComments\'>')[1][:10]
                comments = comments.translate(self.DD)
                
                name = html.split('<title>', 1)[1].split('</title>', 1)[0]

                author = html.split('/" title="Browse ')[1].split('">', 1)[0]

                size = html.split('<dt>Size:</dt>')[1].split('<dd>', 1)[1].split('</dd>')[0]
                size = size.replace('&nbsp;', ' ')

                category = html.split('title="More from this category">')[1].split('</a>', 1)[0]
                category = category.replace('&gt;', '>')

                description = html.split('<div class="nfo">')[1].split('<div class="download">')[0]

                data = {
                        'id': str(count),
                        'category': str(category),
                        'size': str(size),
                        'author': str(author),
                        'name': str(name),
                        'url': str(self.url + str(count)),
                        'comments': int(comments),
                        'leechers': int(leechers),
                        'seeders': int(seeders),
                        'uploaded': str(uploaded_date),
                        'files': int(files_count),
                        'magnet_link': "magnet:?xt=urn:btih:" + str(magnet),
                        'description': str(description)
                        }
                with open('data.json', 'w') as outfile:
                    json.dump(data, outfile)
            except HTTPError:
                self.log('URL not found: ' + self.url + str(count))
            except Exception as e:
                self.log('An unknown error occurred.')
                self.log(e.message)
                continue
            count += 1
        self.scraping = False
