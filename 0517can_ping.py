# coding:utf8
import time
from selenium import webdriver
import mysql.connector
import socket
import urllib
import threading
import requests
'''config={'host':'219.216.64.50',
        'user':'root',
        'password':'123qwe_456',
        'port':3306 ,
        'database':'diting2',
        'charset':'utf8'}'''
config={'host':'127.0.0.1',
        'user':'root',
        'password':'123456',
        'port':3306 ,
        'database':'mydata',
        'charset':'utf8'}
def getIp():
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    # cur.execute("select ip,proxy from proxy_ip1_text where succeed = 1 and ipdns is null" )
    # cur.execute("SELECT dns  FROM proxy_ip1_text a, proxy_ip_dns_relation b WHERE a.ip = b.ip and a.succeed = '1' ")
    cur.execute("SELECT dns FROM  proxy_ip_dns_relation WHERE to_days( create_time) = to_days(now())")
    results = cur.fetchall()
    # print results
    new = []
    for row in results:
        # ip = ''.join(row[0])+":"+row[1]
        ip = row[0]
        new.append(ip)
        # print new
    new = list(set(new))
    cur.close()
    conn.commit()
    conn.close()
    # print new
    return  new

def thread(list1):
    threads = []
    for i in range(0, 20):
        threads.append(threading.Thread(target=pagecode, args=(list1[i * len(list1) / 20:(i + 1) * len(list1) / 20])))
    for i in threads:
        i.start()
        time.sleep(2)
    for i in threads:
        i.join()
        time.sleep(2)
global list2
list2 = []
def pagecode(*t):
    # driver = webdriver.Chrome()
    l1 = []
    global list2
    l = list(t)
    # l.remove('http://www.cnvd.org.cn/flaw/show/CNVD-2018-02779')
    while len(l):
        s1 = l.pop()
        print 'last:', len(l)
        url = 'http://' + s1
        proxies = {
            "http": None,
            "https": None,
        }
        print url
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        # print 1
        try:
            res = requests.get(url, proxies=proxies, headers=headers,timeout = 5).status_code
        # res = driver.get(url).status_code
            print res
            if res == 200:
                l1.append(url)
        except:continue
        # print res
    print '200:',l1
    list2 = l1 + list2
    print 'totle:',list2
thread(getIp())
