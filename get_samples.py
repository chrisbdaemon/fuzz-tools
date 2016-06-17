#!/usr/bin/env python3

import hashlib
import urllib.request
import re
from bs4 import BeautifulSoup

url = "https://wiki.wireshark.org/SampleCaptures"
url_list = []

html_page = urllib.request.urlopen(url)
soup = BeautifulSoup(html_page, "html.parser")
for link in soup.findAll('a'):
    url = link.get('href')
    if '.cap' in url or '.pcap' in url:
        if 'http' not in url or url[0] == '/':
            url = "https://wiki.wireshark.org" + url
        if 'SampleCaptures' in url and 'do=view' in url:
            url = url.replace('do=view', 'do=get')
        url_list.append(url)

print("Total URLS: %d" % len(url_list))

cur_i = 0
for url in url_list:
    cur_i += 1
    print("Downloading %03d/%03d: %s" % (cur_i, len(url_list), url))
    try:
        r = urllib.request.urlopen(url)
        body = r.read()
    except:
        print("Unable to download " + url)
        continue

    filename = "samples/" + hashlib.sha256(body).hexdigest()

    f = open(filename, "wb")
    f.write(body)
    f.flush()
    f.close()
