#!/usr/bin/env python

##
## my apologies for the code that follows
##

import lxml.html
import requests
import sqlite3
import time
import re

# In[333]:


BASE_URL = 'https://wdfw.wa.gov'


# In[334]:


RE_COUNTY = re.compile('([a-zA-Z]+)\n')
RE_ACREAGE = re.compile('([0-9]+.[0-9]+) ?ac.')
RE_ELEVATION = re.compile('([0-9.]+) ?ft.')
RE_TRS = re.compile('([A-Z0-9]+ [A-Z0-9]+)\n')
RE_LAT = re.compile('([0-9.]+),')
RE_LONG = re.compile(', ?([\-0-9.]+)')


# In[475]:


def get_page(page, modifier='high'): 
    """
    returns a list of urls to individual lake pages
    first page is page 0
    modifier can be 'high' or 'lowland' (defaults to high)
    """
    page_url = BASE_URL + "/fishing/locations/" + modifier + "-lakes?name=&county=All&species=&page=" + str(page)
    html = requests.get(page_url)
    document = lxml.html.fromstring(html.content)
    links = [BASE_URL + l.get('href') for l in document.xpath('//td/a[@hreflang="en"]')]
    return links
    


# In[492]:


def get_lake_details(url):
    html = requests.get(url)
    document = lxml.html.fromstring(html.content)
    info = document.xpath('//div[@class="cell large-6 lake-body"]/p/text()')
    info = '\n'.join([i.strip() for i in info if i.strip() != ''])
    
    lake = {
        'name' : document.xpath('//section[@id="block-wdfw-page-title"]/h1')[0].text_content().strip('\n')
    }
    
    try: 
        lake['fish'] = [{'species':f.text_content(), 'url':BASE_URL + f.get('href')} for f in document.xpath('//ul/li[@class="field-item"]/a')]
    except Exception as e:
        print(e)
    
    try:
        lake['county'] = RE_COUNTY.search(info).group().strip()
    except Exception as e:
        print(e)
    
    try:
        lake['acreage'] = RE_ACREAGE.search(info).group().strip()
    except Exception as e:
        print(e)
        
    try:
        lake['elevation'] = RE_ELEVATION.search(info).group().strip()
    except Exception as e:
        print(e)
        
    try: 
        lake['TRS'] = RE_TRS.search(info).group().strip()
    except Exception as e:
        print(e)
        
    try: 
        lake['lat'] = RE_LAT.search(info).group().strip()[:-1]
    except Exception as e:
        print(e)
        
    try: 
        lake['long'] = RE_LONG.search(info).group().strip()[2:]
    except Exception as e:
        print(e)
    
    return lake


# In[467]:


def get_overabundant_page(page):
    page_url = BASE_URL + "/fishing/locations/high-lakes/overabundant?name=&county=All&species=&page=" + str(page)
    html = requests.get(page_url)
    document = lxml.html.fromstring(html.content)
    lakes = document.xpath('//td/a[@hreflang="en"]/text()')
    return lakes


# In[465]:


def get_overabundant_lakes():
    lakes = []
    for i in range(0, 10):
        lakes += get_overabundant_page(i)
    return lakes


# In[468]:


overabundant = get_overabundant_lakes()


# In[338]:


con = sqlite3.connect('highlakes.db')


# In[339]:


db = con.cursor()


# In[340]:


# retrieve all (high) lakes from wdfw website -> this takes forever
def get_all_lakes():
    lakes = []
    print('retrieving lakes...')
    for i in range(0,54):
        print('page ' + str(i+1) + ' out of 54')
        page = get_page(i)
        for lake in page:
            lakes.append(get_lake_details(lake))
            time.sleep(1)
    return lakes


# In[341]:


lakes = get_all_lakes()


# In[495]:


# clean up any missing keys before db inserts (oops)
for lake in lakes:
    if not 'name' in lake:
        lake['name'] = ''
    if not 'county' in lake:
        lake['county'] = ''
    if not 'acreage' in lake:
        lake['acreage'] = ''
    if not 'elevation' in lake:
        lake['elevation'] = ''
    if not 'TRS' in lake:
        lake['TRS'] = ''
    if not 'lat' in lake:
        lake['lat'] = ''
    if not 'long' in lake:
        lake['long'] = ''


# In[498]:


# insert results into DB
for lake in lakes:
    # check to see if lake is already added
    db.execute("SElECT id FROM lakes WHERE name = ?", [lake['name']])
    if len(db.fetchall()) > 0:
        continue
    # add lake to db
    db.execute("INSERT INTO lakes (name, county, acreage, elevation, TRS, lat, long) VALUES (?, ?, ?, ?, ?, ?, ?)", [lake['name'], lake['county'], lake['acreage'][:-4], lake['elevation'][:-4], lake['TRS'], lake['lat'], lake['long']])
    lake_id = db.lastrowid
    # add all fish species to db
    for fish in lake['fish']:
        db.execute("SELECT id FROM fishes WHERE species=?", [fish['species']])
        result = db.fetchall()
        if len(result) == 0:
            db.execute("INSERT INTO fishes (species, url) VALUES (?, ?)", [fish['species'], fish['url']])  
            fish_id = db.lastrowid
        else:
            fish_id = result[0][0]
        db.execute("INSERT INTO fish_lake (fishID, lakeID) VALUES (?, ?)", [fish_id, lake_id])
con.commit()


# In[499]:


# mark overabundant lakes
for lake in overabundant:
    db.execute("UPDATE lakes SET overabundant = 1 WHERE name = ?", [lake])
con.commit()
