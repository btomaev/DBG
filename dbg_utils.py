#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests, time, datetime, asyncio, re, json, random
import httplib2
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from data import *

table = {}
pl_names = []
pl_types = []
pl_teams = []
pl_leggits = []
pl_mints = []
pl_seasons = []
pl_tiers = []
pl_users = []
pl_score = []
index = []
last_user = ''
grade = 0
counter = 0
driver = None
ready = True
request_driver = None
old_raw_messages = None
timing = datetime.datetime.now()
file_name = ""
names = []
wait = 0

def begin():
    global table, pl_names, pl_types, pl_teams, pl_leggits, pl_mints, pl_seasons, pl_tiers, pl_users, pl_score, last_user, index, counter, grade, ready
    table = {}
    pl_names = []
    pl_types = []
    pl_teams = []
    pl_leggits = []
    pl_mints = []
    pl_seasons = []
    pl_tiers = []
    pl_users = []
    pl_score = []
    emty = []
    info = []
    index = []
    last_user = ''
    counter = 0
    grade = 0
    ready = True

def setup(f_name, waitfor, name_list):
    global driver, request_driver, old_raw_messages, file_name, wait, names
    begin()
    file_name = f_name
    wait = waitfor
    names = name_list
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox") # linux only
    if(open("config.txt","r").read()=="headless"):
        chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=3') 
    # chrome_options.add_argument('--proxy-server=180.247.131.229:8080')
    driver = webdriver.Chrome(options=chrome_options)
    # cookies = list(open("cookies.dmp", "r").read())
    # for cookie in cookies:
    #     driver.add_cookie(cookie)
    driver.get("https://discord.com/login")
    driver.add_cookie({'domain': 'discord.com', 'expiry': 1797315530, 'httpOnly': True, 'name': '__sdcfduid', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '089b07815e3811ecbff509ac79d83bbb3566d964bcc7f465a9be3fa7debed3bc44f97f7071e4cb278374ef922adc7206'})
    driver.add_cookie({'domain': 'discord.com', 'expiry': 1797315530, 'httpOnly': True, 'name': '__dcfduid', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '089b07805e3811ecbff509ac79d83bbb'})
    driver.get("https://discord.com/login")
    driver.find_element(By.NAME, "email").send_keys(payload["email"])
    driver.find_element(By.NAME, "password").send_keys(payload["password"])
    driver.find_element(By.XPATH, "//button/following-sibling::button").click()
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//a[@href='/channels/@me/910776657827201034']")))
    time.sleep(1)
    driver.find_element(By.XPATH, "//a[@href='/channels/@me/910776657827201034']").click()
    time.sleep(1)
    old_raw_messages = driver.find_element(By.XPATH, "//ol[@data-list-id='chat-messages']").find_elements(By.XPATH, "//li")

    request_driver = webdriver.Chrome(options=chrome_options)
    request_driver.get("https://discord.com/login")
    request_driver.find_element(By.NAME, "email").send_keys(payload["email"])
    request_driver.find_element(By.NAME, "password").send_keys(payload["password"])
    request_driver.find_element(By.XPATH, "//button/following-sibling::button").click()
    time.sleep(1)
    # request_driver = webdriver.Chrome(options=req_chrome_options)
    # request_driver.get("https://discord.com/login")
    # request_driver.find_element(By.NAME, "email").send_keys(payload["email"])
    # request_driver.find_element(By.NAME, "password").send_keys(payload["password"])
    # request_driver.find_element(By.XPATH, "//button/following-sibling::button").click()
    # WebDriverWait(request_driver, 30).until(EC.presence_of_element_located((By.XPATH, "//a[@href='/channels/@me/910776657827201034']")))
    # time.sleep(1)
    # request_driver.find_element(By.XPATH, "//div[@href='/channels/874340202661961739/912354556350988359']").click()
    # time.sleep(1)
    # request_driver.find_element(By.XPATH, "//a[@href='/channels/874340202661961739/908170421306806272']").click()
    # open("cookies.dmp","w").write(str(driver.get_cookies()))
    print("\n=====================\nБот запущен, все ОК!\n=====================\n")

async def update():
    global old_raw_messages, table, file_name, wait, names
    global table, pl_names, pl_types, pl_teams, pl_leggits, pl_mints, pl_seasons, pl_tiers, pl_users, pl_score, last_user, index, counter
    raw_messages = driver.find_element(By.XPATH, "//ol[@data-list-id='chat-messages']").find_elements(By.XPATH, "//li")
    if(len(raw_messages) == len(old_raw_messages)):
        pass
    else:
        new_messages = list(set(raw_messages) - set(old_raw_messages))
        for message in new_messages:
            # data = message.find_element(By.XPATH, "//div").find_element(By.XPATH, "//div").find_element(By.XPATH, "//div").find_element(By.XPATH, "//div").find_element(By.XPATH, "//div")
            # print(data.text)
            # print("\n\n\n")
            # input()
            msg = message.text
            team = 'None'
            is_target = False
            dt = []
            ctypes = []
            for tm in teams:
                if(tm in msg):
                    team = tm
            if("User: " in msg):
                user = msg[msg.find("User: ")+6:msg[msg.find("User: ")+6:].find("\n")+(len(msg)-len(msg[msg.find("User: ")+6:]))]
            for name in names:
                if(user in name.lower()):
                    is_target = True
            if(not is_target):
                return False
            data = {}
            for item in types:
                if(item+"\n" in msg):
                    ctypes.append(item)
            ctypes.append("Arbaitung")
            if("Mementos" in msg):
                for pos in msg[msg.find("Mementos\n")+8:msg.find(ctypes[0]+"\n")].split("\n"):
                    if('(' in pos and ')' in pos and ':' in pos):
                        for item in types:
                            if("("+item+")" in pos):
                                dt.append(get_data(pos.replace(":fire:",""),item,team))
                data.update({"players": dt})
            for i in range(0,len(ctypes)-1):
                for pos in msg[msg.find(ctypes[i]+"\n")+len(ctypes[i]+"\n"):msg.find(ctypes[i+1]+"\n")].split("\n"):
                    if('(' in pos and ')' in pos and ':' in pos):
                        dt.append(get_data(pos.replace(":fire:",""),ctypes[i],team))
                data.update({"players": dt})

            if(last_user==user):
                pass
            else:
                last_user = user
                header = 'None'
                counter = 1
                for head in headers:
                    if(user in head.lower()):
                        header = head
                pl_names.append("redify"+header) 
                index.append('redify#')
                pl_teams.append('redify')
                pl_leggits.append('redify')
                pl_mints.append('redify')
                pl_seasons.append('redify')
                pl_tiers.append('redify')
                pl_score.append('redify')
                pl_users.append('redify')
            for item in data["players"]:
                pl_names.append(item["name"])
                pl_teams.append(item["team"])
                pl_leggits.append(item["leggit"])
                pl_mints.append(item["mint"])
                pl_seasons.append(item["season"])
                pl_tiers.append(item["type"])
                pl_score.append(item["fanscore"])
                pl_users.append(user)
                index.append(str(counter))
                counter += 1
            table.update({
                'Player name':pl_names,
                'Team':pl_teams,
                'Mint':pl_mints,
                'Legit':pl_leggits,
                'Tier':pl_tiers,
                'Fan Score':pl_score,
                'Season':pl_seasons
                })
        df = pd.DataFrame(table, index=index)
        df.style.applymap(highlight)
        # df.to_excel('./'+file_name+'.xlsx', sheet_name='Legits', index=True)
        df.to_html('./'+file_name+'.html', index=True)
        html = open('./'+file_name+'.html', "r").read()
        open('./'+file_name+'.html', "w").write(unistyle+"\n"+html.replace("<td>redify","<td class='redify'>").replace("<th>redify","<td class='redify'>"))
    old_raw_messages = raw_messages

async def request():
    global request_driver, timing, grade, ready, names, file_name, wait
    if(len(request_driver.find_elements(By.XPATH, "//*[text()='Legit FanScores Complete!']"))>0):
        ready = True
        if(grade > len(names)-1):
            grade = 0 
            print("\n=====================\nПарсинг завершен!\n=====================\n")
            files = {'file': open('./'+file_name+'.html','rb')}
            print(requests.post("http://uplandia.pythonanywhere.com/lgtupdate", files=files).text)
            timing = datetime.datetime.now()+datetime.timedelta(minutes = wait)
            begin()
    if(datetime.datetime.now() >= timing and ready):
        if(grade == 0):
            begin()
            print("\n=====================\nStarting requests...\n=====================\n")
            ready = False
            # random.shuffle(names)
        request_driver.get("https://discord.com/channels/874340202661961739/908170421306806272")
        WebDriverWait(request_driver, 30).until(lambda d: d.find_element(By.XPATH, "//div[@role='textbox']"))
        print("\n=====================\nRequesting: "+names[grade]+"\n=====================\n")
        elem = request_driver.find_element(By.XPATH, "//div[@role='textbox']")
        elem.send_keys("/legits fanscores upland_name:"+names[grade].lower())
        time.sleep(1)
        elem.send_keys(Keys.TAB)
        elem.send_keys(Keys.ENTER)
        grade += 1
        ready = False

def get_data(pos, ptype, pteam):
    player = 'None'
    season = 'None'
    leggit = 'None'
    fanscore = 'None'
    for pl in players:
        if(pl.upper() in pos):
            player = pl
    for lgg in leggits:
        if(lgg.upper() in pos):
            leggit = lgg
    for ss in seasons:
        if(ss in pos[pos.find(")")+1:pos.find(":")]):
            season = ss
    if("- " in pos):
        fanscore = pos[pos.find("- ")+2:]
    elif(": " in pos):
        fanscore = pos[pos.find(": ")+2:]
    return {"mint": pos[pos.find("(")+1:pos.find(")")], "name": player, "leggit": leggit, "season": season[2:], "type": ptype, 'team': pteam, "fanscore": fanscore}


def highlight(s):
    is_it = s.index.get_level_values(1) == '#'
    return 'background-color: red'