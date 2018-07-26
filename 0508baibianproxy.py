# coding=utf-8
from datetime import datetime
import datetime
import urllib
import urllib2
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

def getpage(driver):

    driver.get('https://www.baibianip.com/home/free.html')
    # time.sleep(5)
    # print driver.page_source.encode('utf-8')
    return  driver.page_source.encode('utf-8')

def insertMysql(list):
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute(sql_insertq, list)
    cur.close()
    conn.commit()
    conn.close()

def judgePage(pagesoure):  # <div class="agile-database-form">
    l1 = getIp()
    dict1 = {'ip': '', 'proxy': '', 'add': '', 'unname': '', 'type': '', 'speed': '', 'connecttime': '',
             'alivedays': '', 'testdays': '1'}

    soup = BeautifulSoup(pagesoure, 'lxml')
    tr = soup.find_all("tr")  # <table class="table table-striped table-bordered">
    for i in range(1, len(tr)):
        # print tr[i]
        # print tr[1].text.encode('utf-8')
        td = tr[i].find_all('td')
        dict1['ip'] = td[0].text.split(';')[1]
        dict1['proxy'] = td[1].text
        dict1['add'] = td[2].text
        dict1['type'] = td[5].text
        dict1['speed'] = td[6].text
        dict1['connecttime'] = td[7].text
        dict1['source'] = 'baibian'
        if dict1['ip'] not in l1:
            print dict1
            insertMysql(dict1)


def strat():
    driver = webdriver.Chrome()
    driver.get('https://www.baibianip.com/home/free.html')
    while True:
        time.sleep(600)
        driver.refresh()
        print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        judgePage(driver.page_source)
        # judgePage(getpage(driver))

if __name__ == '__main__':
    strat()