# coding=utf-8
from datetime import datetime
import datetime
import urllib

import time
from bs4 import BeautifulSoup
import mysql.connector
import threading
import socket
import requests
from selenium import webdriver
User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'

sql_insertq = "insert into proxy_ip1_text(ip,proxy,type,unname,speed,connecttime,alivedays,address,testdays,source)values( %(ip)s,%(proxy)s,%(type)s,%(unname)s,%(speed)s,%(connecttime)s,%(alivedays)s,%(add)s,%(testdays)s,%(source)s)"



config = {'host': '127.0.0.1',
          'user': 'root',
          'password': '123456',
          'port': 3306,
          'database': 'mydata',
          'charset': 'utf8'}

def insertMysql(list):
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute(sql_insertq, list)
    cur.close()
    conn.commit()
    conn.close()

def getpage():
    driver = webdriver.Chrome()
    driver.get('http://www.mogumiao.com/web')

    time.sleep(5)
    # print driver.page_source.encode('utf-8')
    return driver.page_source.encode('utf-8')

def getIp():
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("select ip from  proxy_ip1_text " )
    # cur.execute("select ip,proxy from proxy_ip1_text")
    results = cur.fetchall()
    new = []
    for row in results:
        new.append(row[0])
    new = list(set(new))
    cur.close()
    conn.commit()
    conn.close()
    # print new
    return  new

def judgePage(pagesource):  # <div class="agile-database-form">
    # dict1 = {}
    l1 = getIp()
    dict1 = {'ip': '', 'proxy': '', 'add': '', 'unname': '', 'type': '', 'speed': '', 'connecttime': '',
             'alivedays': '', 'testdays': '1'}

    soup = BeautifulSoup(pagesource, 'lxml')
    tr = soup.find_all("tr")  # <table class="table table-striped table-bordered">
    for i in range(1, len(tr)):
        l2 = []
        # print tr[i]
        if i == 6:
            continue
        else:
            # print tr[i]
            td = tr[i].find_all('td')
            try:
                dict1['ip'] = td[0].text
                dict1['proxy'] = td[1].text
                dict1['source'] = 'mogumiao'
                print dict1
                if dict1['ip'] not in l1 and dict1['ip'] not in l2:
                    print dict1
                    l2.append(dict1['ip'])
                    insertMysql(dict1)
            except:
                print tr
                continue

def judgebadpage(pagesource):
    soup = BeautifulSoup(pagesource, 'lxml')
    # print soup.find_all(id = 'error')
    if len(soup.find_all(id = 'error') )== 0:
        # print soup.find_all(id = 'error')
        return True
    else:return False

def strat():
    driver = webdriver.Chrome()
    driver.get('http://www.mogumiao.com/web')
    while True:
        time.sleep(150)
        driver.refresh()
        time.sleep(5)
        print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # try:
        if judgebadpage(driver.page_source) == True:
            judgePage(driver.page_source)
        else:
            driver = webdriver.Chrome()
            driver.get('http://www.mogumiao.com/web')
            continue
        # except Exception, e:
        #     print Exception, ":", e
        #     print BaseException.message
        #     continue
        # judgePage(getpage(driver))

if __name__ == '__main__':
    strat()
    # driver = webdriver.Chrome()
    # driver.get('http://www.mogumiao.com/web')
    # if judgebadpage(driver.page_source) == True:
    #     judgePage(driver.page_source)
    # judgePage(driver.page_source)