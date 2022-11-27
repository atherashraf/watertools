# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 12:05:28 2022

@author: timhe
"""
import requests
import re
import os
import urllib
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import watertools

Horizontal = 24
Vertical = 6
output_folder = r"temp"

username, password = watertools.Functions.Random.Get_Username_PWD.GET('NASA')

url = "https://e4ftl01.cr.usgs.gov/MOLT/MOD13Q1.061/2021.12.19/"
f = urllib.request.urlopen(url)

# Sum all the files on the server
soup = BeautifulSoup(f, "lxml")
for i in soup.findAll('a', attrs={'href': re.compile('(?i)(hdf)$')}):

    # Find the file with the wanted tile number
    Vfile = str(i)[30:32]
    Hfile = str(i)[27:29]
    if int(Vfile) is int(Vertical) and int(Hfile) is int(Horizontal):
        nameDownload = urllib.parse.urljoin(url, i['href'])
        print(nameDownload)

        file_name = os.path.join(output_folder, nameDownload.split('/')[-1])
        print(file_name)

        x = requests.get(nameDownload, allow_redirects=False)
        y = requests.get(x.headers['location'], auth=(username, password))
        z = open(file_name, 'wb')
        z.write(y.content)
        z.close()
        statinfo = os.stat(file_name)
        print(statinfo)
