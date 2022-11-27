import urllib
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

f = urllib.request.urlopen("https://e4ftl01.cr.usgs.gov/MOLT/MOD13Q1.061/2021.12.19/")
soup = BeautifulSoup(f, "lxml")
print(soup)