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

sql_insertq = "insert into proxy_ip1_text(ip,proxy,type,unname,speed,connecttime,alivedays,address,testdays,source)values( %(ip)s,%(proxy)s,%(type)s,%(unname)s,%(speed)s,%(connecttime)s,%(alivedays)s,%(add)s,%(testdays)s,%(source)s)"

header = {}
header['User-Agent'] = User_Agent

config = {'host': '127.0.0.1',
          'user': 'root',
          'password': '123456',
          'port': 3306,
          'database': 'mydata',
          'charset': 'utf8'}

def getIp():
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("select ip,proxy from proxy_ip1_text where testdays >0" )
    # cur.execute("select ip,proxy from proxy_ip1_text")
    results = cur.fetchall()
    # print results
    new = []
    for row in results:
        ip = ''.join(row[0])+":"+row[1]
        new.append(ip)
        # print new
    new = list(set(new))
    cur.close()
    conn.commit()
    conn.close()
    return  new

def validateIp(proxy):
    url = "http://ip.chinaz.com/getip.aspx"
    socket.setdefaulttimeout(10)
    try:
        proxy_host = "http://" + proxy
        proxy_temp = {"http": proxy_host}
        # print 1
        res = urllib.urlopen(url, proxies=proxy_temp).read()
        # print 2
        # print res.status_code
        return True
    except Exception, e:

        return False

def ipjudge(*t):

    list1 = list(t)
    #list1 = t
    for i in range(0,len(list1)):
        print 'last',len(list1)-i,'unjudge'

        if validateIp(list1[i]) == True:
            updateSql(list1[i].split(':')[0])
            print 'succeed',list1[i].split(':')[0]
        else:
            print 'fall',list1[i]
            badSql(list1[i].split(':')[0])

def updateSql(s):
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    # cur.execute("update proxy_ip1_text set testdays = ifnull(testdays,0) + 1 ,updatatime=SYSDATE() where ip = '%s'" %(str(s)))
    cur.execute("update proxy_ip1_text set testdays =1 + testdays ,updatatime=SYSDATE() where ip = '%s'" % (str(s)))
    cur.close()
    conn.commit()
    conn.close()

def badSql(s):
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("update proxy_ip1_text set testdays =0,updatatime=SYSDATE() where ip = '%s'" %(str(s)))
    cur.close()
    conn.commit()
    conn.close()

def thread(list1):
    threads = []
    #list1 = [u'180.121.141.227:26625', u'49.70.32.249:47137', u'180.122.144.50:41017', u'106.46.3.187:47691', u'115.221.120.137:25256', u'27.153.128.133:22354', u'49.74.130.150:8123', u'49.89.86.105:37727', u'114.231.155.206:25494']
    for i in range(0, 40):
        threads.append(threading.Thread(target=ipjudge, args=(list1[i * len(list1) / 40:(i + 1) * len(list1) / 40])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[0:len(list1)/20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[len(list1) / 20:2 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[2 * len(list1) / 20:3 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[3 * len(list1) / 20:4 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[4 * len(list1) / 20:5 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[5 * len(list1) / 20:6 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[6 * len(list1) / 20:7 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[7 * len(list1) / 20:8 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[8 * len(list1) / 20:9 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[9 * len(list1) / 20:10 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[10 * len(list1) / 20:11 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[11 * len(list1) / 20:12 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[12 * len(list1) / 20:13 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[13 * len(list1) / 20:14 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[14 * len(list1) / 20:15 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[15 * len(list1) / 20:16 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[16 * len(list1) / 20:17 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[17 * len(list1) / 20:18 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[18 * len(list1) / 20:19 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=(list1[19 * len(list1) / 20:20 * len(list1) / 20])))
    # threads.append(threading.Thread(target=ipjudge, args=('13')))
    # threads.append(threading.Thread(target=ipjudge, args=('14')))
    # threads.append(threading.Thread(target=ipjudge, args=('15')))
    # threads.append(threading.Thread(target=ipjudge, args=('16')))
    # threads.append(threading.Thread(target=ipjudge, args=('17')))
    # threads.append(threading.Thread(target=ipjudge, args=('18')))
    # threads.append(threading.Thread(target=ipjudge, args=('19')))
    # threads.append(threading.Thread(target=ipjudge, args=('20')))
    for i in threads:
        i.start()
        time.sleep(2)
    for i in threads:
        i.join()
        time.sleep(2)

def insertMysql(list):
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute(sql_insertq, list)
    cur.close()
    conn.commit()
    conn.close()
thread(getIp())