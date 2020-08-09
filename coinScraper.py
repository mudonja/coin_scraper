#!/usr/bin/env/ python
import random
from datetime import datetime
import datetime
import requests
from bs4 import BeautifulSoup, SoupStrainer
# TODO: Implement torrequests so user can use TOR
# from torrequest import TorRequest
import os
import time
import json

# TODO: Secure this before using
# Used for github credentials
usrname = input("Github username:")
passwrd = input("Github password:")

base_url = 'https://coinmarketcap.com'
github_url = "https://" + usrname + ":" + passwrd + "@github.com"

# Load all cryptocurrency relative paths to form cryptocurrency links on Coin Market Cap
i = 1
page_num = 1
currency_pages = dict()

while (True):
    napTime = random.randint(5, 10)
    time.sleep(napTime)
    # TODO: Create a function that will read the url, html tag, class with name(optional?)
    #   and will download based on criteria...
    source_code = requests.get(base_url + "/" + str(page_num) + "/")
    if (source_code.status_code == 200):
        print("Page:", page_num, "\nStatus 200 OK!")
        plain_text = source_code.content
        soup = BeautifulSoup(plain_text, "lxml")
        links = soup.findAll('a', {'class': 'cmc-link'}, href=True)
        for link in links:
            if (link.get('title') != None and "/currencies/" in str(link.get('href'))):
                # print(i, link.get('title'), "\n", link.get('href'))
                currency_pages[link.get('title')] = link.get('href')
                i += 1
        page_num += 1
        #break  # TODO: Remove for full functionality
    elif (source_code.status_code == 404):
        print("Page not found:", source_code.status_code)
        break
    else:
        print("Code:", source_code.status_code)
print("Crypto Currency Total:", i-1)
Download_counter = 1
total = 1
start_time = time.time()
# currency_pages- hold all names and rel paths for every cryptocurrency
# line bellow used for testing
# currency_pages={"Bitcoin":"/currencies/bitcoin/", "Tether":"/currencies/tether/",
#                "FLETA":"/currencies/fleta/", "Hive":"/currencies/hive-blockchain/"}  # Used for testing
tags = dict()  # cryptocurrency tag(key is currency name eg bitcoin)
currency_github = dict()  # crypto currency github links(key is currency name eg bitcoin)
#print(currency_pages)
#stopPT = 0
# This for loop scrapes SourceCode links and Tags
whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
for keytmp, val in currency_pages.items():
    # key=name
    # val=relative path
    '''if (stopPT > 5):  # TODO Remove for functionality
        break
    stopPT += 1'''
    napTime = random.randint(5, 10)
    time.sleep(napTime)
    response = requests.get(base_url + val)
    key = ''.join(filter(whitelist.__contains__, keytmp))
    if (response.status_code == 200):
        print("Status code:", response.status_code)
        print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
        plain_text = response.content
        soup = BeautifulSoup(plain_text, "lxml")
        tgs = soup.findAll('span', attrs={'class': 'cmc-label sc-13jrx81-0 jPpbJm'})
        tmp = []
        for tag in tgs:
            tmp.append(tag.text)
            # print(tag.text)
        tags[key] = tmp
        links = soup.findAll('a', string="Source Code", href=True)
        for link in links:
            currency_github[key] = link.get('href')

        print("Done with TAGS for:", key)
        print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
    else:
        print("Response did not return status 200 OK", "\n", "Response status:", response.status_code)

with open("./codeSimLinks.txt", 'a+') as f:
    f.write(json.dumps(currency_github))
    f.close()

dateTimeObj = datetime.datetime.now()
timestampStr = dateTimeObj.strftime("%Y-%m-%d-%H-%M-%S_%f")
cmc_dir_path = "."
cmc_dir = "CMCcurrencies" + timestampStr
cmc = os.path.join(cmc_dir_path, cmc_dir)
if (os.path.isdir(cmc)):
    print("\nCMCcurrencies already exists!\n")
else:
    print(cmc, "created!")
    os.mkdir(cmc)

#stopPT = 0
print("Going to clone from GitHub\n")
print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
for key, val in currency_github.items():
    '''if (stopPT > 5):  # TODO Remove for functionality
        break
    stopPT += 1'''
    # Cardano has their own weird website, just skip it and TODO clone cardano manually
    if (str(key).lower() == "cardano"):
        continue
    # Stores the path for directory where crypto will be cloned
    currency_dir = os.path.join(cmc, str(key))
    if (os.path.isdir(currency_dir)):
        print(currency_dir, " exists!")
    else:
        print("\nMaking currency_dir:", currency_dir)
        os.mkdir(currency_dir)
    # Write tags to a txt file inside of currency directory
    # TODO Uncomment section bellow in final version
    with open(currency_dir + "/tags.txt", 'w') as f:
        f.write(json.dumps(tags[key]))
        f.close()
    napTime = random.randint(5, 10)
    time.sleep(napTime)
    response = requests.get(val)
    # TODO: Maybe try?
    # Checks weather gihub repository
    if (response.status_code == 200 and "github.com" in response.__getattribute__('url')):
        cnter = 0
        napTime = random.randint(5, 10)
        time.sleep(napTime)
        plain_text = response.content
        soup = BeautifulSoup(plain_text, "lxml")  # , parse_only=SoupStrainer('a'))
        # This one targets only pinned repos
        if (soup.find('h2', {'class': "f4 text-normal flex-auto pr-2"})):
            pinned_repos = soup.find('h2', {'class': "f4 text-normal flex-auto pr-2"}).text.strip().lower()
            if (pinned_repos == "pinned repositories"):
                links = soup.findAll('a', {'class': 'text-bold flex-auto min-width-0'}, href=True)
                print("Pinned Repositories")
                for link in links:
                    # so we only get first 2 dirs(why 2, one is for source the other is for suggestions)
                    # Make the code really smart checks weather changes are in the proposal directory and
                    # increases the score if some errors will get fixed or if code distance increases
                    cmd = "git clone --progress " + github_url + str(
                        link.get('href')) + '.git ' + currency_dir + " 2>>~/currency-clone.log"
                    os.system(cmd)
                    Download_counter = Download_counter + 1
        elif (soup.find('h2', {'class': 'f4 text-normal d-md-none'})):
            regular_repos = soup.find('h2', {'class': 'f4 text-normal d-md-none'}).text.strip().lower()
            if (regular_repos == "repositories"):
                links = soup.findAll('a', itemprop="name codeRepository", href=True)
                print("Regular Repositories")
                for link in links:
                    if (cnter > 1):  # Get only first two repos
                        break
                    cmd = "git clone --progress " + github_url + str(
                        link.get('href')) + '.git ' + currency_dir + " 2>>~/currency-clone.log"
                    os.system(cmd)
                    Download_counter = Download_counter + 1
                    cnter += 1
        else:
            print("Repository")
            cmd = "git clone --progress " + str(val)[:8] + usrname + ":" + passwrd + "@" + str(val)[
                                                                                         8:] + '.git ' + currency_dir + " 2>>~/currency-clone.log"
            os.system(cmd)
            Download_counter = Download_counter + 1
    # Checks weather gitlab repo
    elif (response.status_code == 200 and "gitlab.com" in response.__getattribute__('url')):
        napTime = random.randint(5, 10)
        time.sleep(napTime)
        cmd = "git clone --progress " + str(val)[:8] + usrname + ":" + passwrd + "@" + str(val)[
                                                                                     8:] + '.git ' + currency_dir + " 2>>~/currency-clone.log"
        os.system(cmd)
        Download_counter = Download_counter + 1
    # Checks weather bitbucket repo
    elif (response.status_code == 200 and "bitbucket" in response.__getattribute__('url')):
        print("Error: Not implemented yet")

total = total + 1
napTime = random.randint(5, 10)
time.sleep(napTime)
print("Tried to clone:", Download_counter)
print("---Time elapsed: %s seconds ---" % (time.time() - start_time))

# TODO: Create a gihub module that will keep your passwords secure when cloning from git
# E.g. Create a file that will have a function(is this what a library is?) for you to send password and user
# from program and that function will use it in a secure way(so that your password does not leave your computer
# in a insecure way!!!
