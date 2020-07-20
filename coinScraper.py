#!/usr/bin/env/ python
import random
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
# TODO: Implement torrequests so user can use TOR
# from torrequest import TorRequest
import os
import re
import time
import json

# Used for github credentials
#usrname = input("Github username:")
#passwrd = input("Github password:")


base_url = 'https://coinmarketcap.com'
# Line bellow is important
# TODO Uncomment following
# git_base_url = "https://" + usrname + ":" + passwrd + "@github.com"

# Load all cryptocurrency relative paths to form cryptocurrency links on Coin Market Cap
i=1
page_num=1
currency_pages=dict()

while(True):
    napTime = random.randint(5, 10)
    time.sleep(napTime)
    source_code = requests.get(base_url+"/"+str(page_num)+"/")
    if(source_code.status_code == 200):
        plain_text = source_code.content
        soup = BeautifulSoup(plain_text, "lxml")
        links = soup.findAll('a', {'class': 'cmc-link'},href=True)
        for link in links:
            if(link.get('title')!=None and "/currencies/" in str(link.get('href'))):
                print(i,link.get('title'),"\n",link.get('href'))
                currency_pages[link.get('title')]=link.get('href')
                i+=1
        page_num+=1
        break
    elif(source_code.status_code==404):
        print("Page not found:",source_code.status_code)
        break
    else:
        print("Code:",source_code.status_code)

# TODO: coin gecko has an API to get all tickers with id so use id to access currency and strip data
Download_counter = 1
total = 1
start_time = time.time()
#currency_pages- hold all names and rel paths for every cryptocurrency
#currency_pages={"Bitcoin":"/currencies/bitcoin/","Tether":"/currencies/tether/"}  # Used for testing
tags=dict()  # Store tags for a cryptocurrency(key is currency name eg bitcoin)
currency_github=dict()  # Store github links for each crypto currency(key is currency name eg bitcoin)

# This for loop scrapes SourceCode link and Tags
for key,val in currency_pages.items():
    #key=name
    #val=relative path
    napTime = random.randint(5, 10)
    time.sleep(napTime)
    response = requests.get(base_url + val)
    if (response.status_code == 200):
        plain_text = response.content
        soup = BeautifulSoup(plain_text, "lxml")
        tgs = soup.findAll('span', attrs = {'class' : 'cmc-label sc-13jrx81-0 jPpbJm'})
        tmp=[]
        for tag in tgs:
            tmp.append(tag.text)
            #print(tag.text)
        tags[key]=tmp
        links = soup.findAll('a', string="Source Code", href=True)
        for link in links:
            currency_github[key] = link.get('href')

        #print(tags,'\n',currency_github)
# TODO: clone git repos using currency_github for links
    else:
        print("Response did not return status 200 OK","\n","Response status:",response.status_code)
with open("./codeSimTags.txt",'a+') as f:
    f.write(json.dumps(tags))
    f.close()
with open("./codeSimLinks.txt",'a+') as f:
    f.write(json.dumps(currency_github))
    f.close()





'''

    if len(curr_git) > 1:
        # resp=tr.get(str(curr_git[1]))
        resp = requests.get(str(curr_git[1]))
        soup = BeautifulSoup(resp.text, "html.parser")
        # check for the pinned section
        if (soup.find_all(class_="text-bold flex-auto min-width-0")):
            curr_repo = soup.find_all(class_="text-bold flex-auto min-width-0")
            curr_repo = re.findall("href=\".*\"", str(curr_repo))
            # print(counter,":","CURRENCY_REPO:"+curr_repo[0]+"\n")
            tmp = curr_repo[0].split("\"")
            path = git_base_url + str(tmp[1])
            path.replace(" ", "")
            # print("git clone ",path,"\n")
            # UNCOMMENT LINE BELLOW IN ORDER TO START CLONNING
            currency_dir = str(tmp[1]).replace("/", "_")
            print(Download_counter, ":", currency_dir)
            # os.system('%s %s'  % ('mkdir','~/currencyDB/'+currency_dir))
            ###os.system('%s %s %s %s %s' % (
            #'git', 'clone --progress', path + ".git", "~/currencyRepoDB/" + currency_dir, "2>>~/currency-clone.log"))
            Download_counter = Download_counter + 1
            print("\n")
        # check for regular repo list
        elif (soup.find_all(class_="public source d-block py-4 border-bottom")):
            curr_repo = soup.find_all(class_="public source d-block py-4 border-bottom")
            curr_repo = re.findall("href=\".*\"", str(curr_repo))
            # print(counter,":","CURRENCY_REPO:"+curr_repo[0]+"\n")
            tmp = curr_repo[0].split("\"")
            path = git_base_url + str(tmp[1])
            path.replace(" ", "")
            # print("git clone ",path,"\n")
            currency_dir = str(tmp[1]).replace("/", "_").replace(".", "_")
            print(Download_counter, ":", currency_dir)
            # UNCOMMENT LINE BELLOW IN ORDER TO START CLONNING
            # os.system('%s %s'  % ('mkdir','~/currencyDB/'))
            # os.system('%s %s %s %s' % ('git','clone',path + ".git","~/currencyDB/"+currency_dir))
            ###os.system('%s %s %s %s %s' % (
            #'git', 'clone --progress', path + ".git", "~/currencyRepoDB/" + currency_dir, "2>>~/currency-clone.log"))
            Download_counter = Download_counter + 1
            print("\n")
        else:
            # print(counter,":","CURRENCY_REPO:"+str(curr_git[1])+"\n")
            # print("git clone ", str(curr_git[1]),"\n")
            currency_dir = re.findall("\/[a-z].*", str(curr_git[1]))
            # currency_dir=currency_dir.replace("/","_")
            currency_dir = str(currency_dir[0]).replace("/", "_").replace(".", "_")
            print(Download_counter, ":", currency_dir)
            # UNCOMMENT LINE BELLOW IN ORDER TO START CLONNING
            # os.system('%s %s %s %s' % ('git','clone',str(curr_git[1]),"~/currencyDB/"+currency_dir))
            ###os.system('%s %s %s %s %s' % (
            #'git', 'clone --progress', path + ".git", "~/currencyRepoDB/" + currency_dir, "2>>~/currency-clone.log"))
            Download_counter = Download_counter + 1
            print("\n")
    else:
        print("\nNo Source Code Link Found!" + str(curr_git) + "\n")
    total = total + 1
    napTime = random.randint(5, 10)
    time.sleep(napTime)

print("--- %s seconds ---" % (time.time() - start_time))
'''