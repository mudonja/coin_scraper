#!/usr/bin/env/ python
import random
import requests
import urllib.request
import time
from bs4 import BeautifulSoup, SoupStrainer
# TODO: Implement torrequests so user can use TOR
# from torrequest import TorRequest
import os
import re
import time
import json

# TODO: Secure this before using
# Used for github credentials
usrname = input("Github username:")
passwrd = input("Github password:")


base_url = 'https://coinmarketcap.com'
# Line bellow is important
# TODO Uncomment following
github_url = "https://" + usrname + ":" + passwrd + "@github.com"

# Load all cryptocurrency relative paths to form cryptocurrency links on Coin Market Cap
i=1
page_num=1
currency_pages=dict()

while(True):
    napTime = random.randint(5, 10)
    time.sleep(napTime)
    # TODO: Create a function that will read the url, html tag, class with name(optional?)
    #   and will download based on criteria...
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
        break # TODO: Remove for full functionality
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
# TODO: Remove, Comment out line bellow for code to work
currency_pages={"Bitcoin":"/currencies/bitcoin/", "Tether":"/currencies/tether/",
                "FLETA":"/currencies/fleta/", "Hive":"/currencies/hive-blockchain/"}  # Used for testing
tags=dict()  # Store tags for a cryptocurrency(key is currency name eg bitcoin)
currency_github=dict()  # Store github links for each crypto currency(key is currency name eg bitcoin)

stopPT=0
# This for loop scrapes SourceCode link and Tags
for key,val in currency_pages.items():
    #key=name
    #val=relative path
    if(stopPT>5): # TODO Remove for functionality
        break
    stopPT+=1

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
    else:
        print("Response did not return status 200 OK","\n","Response status:",response.status_code)
'''
with open("./codeSimLinks.txt",'a+') as f:
    f.write(json.dumps(currency_github))
    f.close()
'''
cmc_dir_path="."
cmc_dir = "CMCcurrencies"
cmc = os.path.join(cmc_dir_path,cmc_dir)
if(os.path.isdir(cmc)):
    print("\nCMCcurrencies already exists!\n")
else:
    os.mkdir(cmc)
stopPT=0
for key, val in currency_github.items():
    if (stopPT > 5):  # TODO Remove for functionality
        break
    stopPT += 1
    # Cardano has their own weird website, just skip it and TODO clone cardano manually
    if(str(key).lower()=="cardano"):
        continue
    # Stores the path for directory where crypto will be cloned
    currency_dir = os.path.join(cmc,str(key))
    if(os.path.isdir(currency_dir)):
        print(currency_dir," exists!")
    else:
        print("Making currency_dir:", currency_dir)
        #TODO Uncomment bellow
        #os.mkdir(currency_dir)
    # Write tags to a txt file inside of currency directory
    #TODO Uncomment section bellow in final version
    '''with open(currency_dir+"/tags.txt", 'w') as f:
        f.write(json.dumps(tags[key]))
        f.close()'''

    napTime = random.randint(5, 10)
    time.sleep(napTime)
    response = requests.get(val)
#TODO: Maybe try? I was high while typing this
#This can be a parallel process execution
#One process forks git hub clone in background to work while the other keeps
#loading other values in the queue
#maybe even spawn a separate process at the sime time
#multiple git clone processes in the background so you clone
#multiple repositories at once

    ###START PROGRAMMING PROPERLY AND REDUCE REDUNDANCY!!!!###
    # Checks weather gihub repository
    if (response.status_code == 200 and "github.com" in response.__getattribute__('url')):
        plain_text = response.content
        soup = BeautifulSoup(plain_text, "lxml")#, parse_only=SoupStrainer('a'))
        # This one targets only pinned repositories
        # Its non flexible but it could maybe be made flexible(Adding a
        # variable(a single point) where user can specify the code that a pinned section has
        cnter = 0
        try:
            pinned_repos=soup.find('h2', {'class': "f4 text-normal flex-auto pr-2"}).text.strip().lower()
            if (pinned_repos == "pinned repositories"):
                links = soup.findAll('a', {'class': 'text-bold flex-auto min-width-0'}, href=True)
                for link in links:
                    # so we only get first 2 dirs(why 2, one is for source the other is for suggestions)
                    # Make the code really smart checks weather changes are in the proposal directory and
                    # increases the score if some errors will get fixed or if code distance increases
                    if (cnter > 2):
                        break
                    print("git clone", github_url + str(link.get('href') + '.git'))
        except AttributeError:
            print("Could not find pinned section...")
            pass
        try: # TODO: YOU ARE HERE....FIGURING OUT HOW TO SEPARATE PINNED NON PINNED AND OTHRES FROM EACHOTHER
            regular_repos = soup.find('h2', {'class': 'f4 text-normal d-md-none'}).text.strip().lower()
            if (regular_repos == "repositories"):
                links = soup.findAll('a', itemprop="name codeRepository", href=True)
                for link in links:
                    # so we only get first 2 dirs(why 2, one is for source the other is for suggestions)
                    # Make the code really smart checks weather changes are in the proposal directory and
                    # increases the score if some errors will get fixed or if code distance increases
                    if (cnter > 2):  # Get only first two repos
                        break
                    print("git clone", github_url + str(link.get('href') + '.git'))
                    cnter += 1
        except AttributeError:
            print("Did not find multiple directories...")
            pass
        finally:
            print("git clone", github_url+str(link.get('href')+'.git'))
            #if (link.get('title') != None and "/currencies/" in str(link.get('href'))):
            #    print(i, link.get('title'), "\n", link.get('href'))
            #    currency_pages[link.get('title')] = link.get('href')
                #git clone link+.git
    # Checks weather gitlab repo
    elif(response.status_code == 200 and "gitlab.com" in response.__getattribute__('url')):
        plain_text = response.content
        soup = BeautifulSoup(plain_text, "lxml", parse_only=SoupStrainer('a'))
        links = soup.findAll('a', {'class': 'text-bold flex-auto min-width-0'}, href=True)
        for link in links:
            #TODO: Check if this needs updating...how does gitlab works
            print("git clone", github_url + str(link.get('href') + '.git'))
            # if (link.get('title') != None and "/currencies/" in str(link.get('href'))):
            #    print(i, link.get('title'), "\n", link.get('href'))
            #    currency_pages[link.get('title')] = link.get('href')
            # git clone link+.git
    # Checks weather bitbucket repo
    elif(response.status_code == 200 and "bitbucket" in response.__getattribute__('url')):
        print("Error: Not implemented yet")

'''<input type="text" class="form-control input-monospace input-sm" data-autoselect="" value="https://github.com/sfluo/sdnexp.git" aria-label="Clone this repository at https://github.com/sfluo/sdnexp.git" readonly="">'''

'''
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
    # 'git', 'clone --progress', path + ".git", "~/currencyRepoDB/" + currency_dir, "2>>~/currency-clone.log"))
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
    # 'git', 'clone --progress', path + ".git", "~/currencyRepoDB/" + currency_dir, "2>>~/currency-clone.log"))
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
    # 'git', 'clone --progress', path + ".git", "~/currencyRepoDB/" + currency_dir, "2>>~/currency-clone.log"))
    Download_counter = Download_counter + 1
    print("\n")


total = total + 1
napTime = random.randint(5, 10)
time.sleep(napTime)
'''
print("--- %s seconds ---" % (time.time() - start_time))

#TODO: Create a gihub module that will keep your passwords secure when cloning from git
# E.g. Create a file that will have a function(is this what a library is?) for you to send password and user
# from program and that function will use it in a secure way(so that your password does not leave your computer
# in a insecure way!!!