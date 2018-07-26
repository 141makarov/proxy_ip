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

User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
#sql_insert = "insert into phish(pid,url,submitted,valid,addtime)values( %(pid)s,%(url)s,%(submitted)s,%(valid)s,%(online)s,%(addtime)s)"
sql_insert = "insert into phish(pid,url,submitted,valid,online,addtime)values( %(pid)s,%(url)s,%(submitted)s,%(valid)s,%(online)s,%(addtime)s)"
header = {}
header['User-Agent'] = User_Agent

config = {'host': '127.0.0.1',
          'user': 'root',
          'password': '123456',
          'port': 3306,
          'database': 'mydata',
          'charset': 'utf8'}

def insertMysql(list):
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute(sql_insert, list)
    cur.close()
    conn.commit()
    conn.close()

def getpage(url1,i):
    while True:
        try:
            session = requests.Session()
            session.trust_env = False

            response = session.get(url='https://www.phishtank.com/phish_archive.php?page='+str(i), params=i)
            # response = requests.get(url='https://www.phishtank.com/phish_archive.php?page='+str(i), params=i)

            break
        except:
            print 'bad page'
            continue

    return response.text

def getpidl():
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("select pid from phish order by pid desc LIMIT 0,1" )
    results = cur.fetchall()
    # print results[0][0]
    cur.close()
    conn.commit()
    conn.close()
    return  results[0][0]

def judgePage(pagesource,recordpid):

    dict1 = {'pid':'','url' :'','submitted':'','valid':'','online':'','addtime':''}
    soup = BeautifulSoup(pagesource, 'lxml')
    tr = soup.find_all('tr')
    for i in range(1,len(tr)):
        td =  tr[i].find_all('td')
        try:
            dict1['pid'] = str(td[0].text)
            dict1['addtime'] = str(td[1].contents[2].text)
            dict1['url'] = str(td[1].contents[0])
            dict1['submitted'] = str(td[2].text)
            dict1['valid'] = str(td[3].text)
            dict1['online'] = str(td[4].text)
            print dict1
            if int(dict1['pid']) > int(recordpid):
                #print 1
                insertMysql(dict1)
            else:
                #print 2
                return False
        except :continue

def writeRecord(record):
    fp  = open("phish.txt", 'w+')
    fp.writelines(str(record))
    fp.close()
    print "updata record"

def readRecord():
    fp = open("phish.txt", 'r+')
    record = fp.read()
    fp.close()
    return record

def start():
    url = 'https://www.phishtank.com/phish_archive.php?page='
    #page = 7266
    recordpid = getpidl()
    #page = int(readRecord())
    page = 1
    # recordpid = 5491002
    while True:
        if   judgePage(getpage(url,page),recordpid) == False:
            break
        else:
            page +=1
            writeRecord(page)
            print 'now page:',page
            continue


start()
#getpidl()