# coding=utf-8
#判断是否能ping通
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

sql_insertq = "insert into proxy_ip1_text(ip,proxy,type,unname,speed,connecttime,alivedays,address,testdays)values( %(ip)s,%(proxy)s,%(type)s,%(unname)s,%(speed)s,%(connecttime)s,%(alivedays)s,%(add)s,%(testdays)s)"

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
    cur.execute(sql_insertq, list)
    cur.close()
    conn.commit()
    conn.close()

def timeStampnow(data):
    timeArray = time.strptime(data, "%y-%m-%d %H:%M")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

def timeStamp(data):
    timeArray = time.strptime(data, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

def interRegional(now, first, last):
    if first - now >= 0 and now - last > 0:
        return True
    else:
        return False

def getpage(url1,i):
    url = url1 + str(i)
   # url = 'http://www.xicidaili.com/nn/' + str(i)
    req = urllib2.Request(url, headers=header)
    res = urllib2.urlopen(req).read()
    return res



def judgePage(url_list):
    dict1 = {'ip': '', 'proxy': '', 'add': '', 'unname': '', 'type': '', 'speed': '', 'connecttime': '',
             'alivedays': '','testdays':'1'}
    page = 1
    list1 = []

    count = 1
    for url in url_list:
        print 'finding url：',url
        while True:
            pagesoure = getpage(url,page)
            soup = BeautifulSoup(pagesoure, 'lxml')
            ips = soup.findAll('tr')
            for x in range(1, len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                now = timeStampnow(tds[9].text)
                last = timeStamp(str(datetime.date.today() - datetime.timedelta(days=2)))  # 至当前日期减y天
                first = timeStamp(str(datetime.date.today() - datetime.timedelta(days=1)))  # 从当前日期减x天
                if interRegional(now, first, last) == True:
                    # dict1['ip'] = tds[1].text
                    #if validateIp(proxy_ip) == True:
                        proxy_ip = tds[1].text + ':'+tds[2].text
                        dict1['ip'] = tds[1].text
                        dict1['proxy'] = tds[2].text
                        dict1['add'] = tds[3].text.replace(' ', '')
                        dict1['unname'] = tds[4].text
                        dict1['type'] = tds[5].text
                        dict1['speed'] = tds[6].div['title']
                        dict1['connecttime'] = tds[7].div['title']
                        dict1['alivedays'] = tds[8].text
                        print tds[9].text
                        ptoxy_temp = dict1['ip']+':'+dict1['proxy']
                        list1.append(ptoxy_temp)
                        print dict1
                        print 'total count',count
                        count += 1
                        insertMysql(dict1)

            if compareTime(last, now) == False:
                    print 'last page data', tds[9].text
                    break
            else:
                    page += 1

def interRegional(now, first, last):
    if first - now >= 0 and now - last > 0:
        return True
    else:
        return False

def compareTime(record, now):
    if now - record > 0:
        return True
    else:
        return False

def updateSql(s):
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    # cur.execute("update proxy_ip1_text set testdays = ifnull(testdays,0) + 1 ,updatatime=SYSDATE() where ip = '%s'" %(str(s)))
    cur.execute("update proxy_ip1_text set succeed = 1 ,updatatime=SYSDATE() where ip = '%s'" % (str(s)))
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

        #continue

def getIp():
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("select ip,proxy from proxy_ip1_text where succeed = 0 " )#and to_days(updatatime) = to_days(now())
    # cur.execute("select ip,proxy from proxy_ip1_text")
    results = cur.fetchall()
    new = []
    for row in results:
        ip = ''.join(row[0])+":"+row[1]
        new.append(ip)
    new = list(set(new))
    cur.close()
    conn.commit()
    conn.close()
    return  new

def getIpnull():
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("select ip,proxy from proxy_ip1_text where succeed = 1" )
    results = cur.fetchall()
    new = []
    for row in results:
        ip = ''.join(row[0])+":"+row[1]
        new.append(ip)
    new = list(set(new))
    cur.close()
    conn.commit()
    conn.close()
    return  new

def ipjudge(*t):

    list1 = list(t)
    #list1 = t
    l1 = []
    for i in range(0,len(list1)):

        # print l1
        print 'last',len(list1)-i,'unjudge'

        if validateIp(list1[i]) == True:
            updateSql(list1[i].split(':')[0])
            print 'succeed',list1[i]


        else:
            print 'fall',list1[i]

            # badSql(list1[i].split(':')[0])

def ipjudgenull(*t):

    #list1 = list(t)
    list1 = t[0]
    print t
    for i in range(0,len(list1)):
        print 'last',len(list1)-i,'unjudge'

        if validateIp(list1[i]) == True:
            updateSql(list1[i].split(':')[0])
            print 'succeed', list1[i].split(':')[0]
        else:
            print 'fall and delete', list1[i]
            badSql(list1[i].split(':')[0])

def thread(list1):
    threads = []
    for i in range(0, 40):
        threads.append(threading.Thread(target=ipjudge, args=(list1[i * len(list1) / 40:(i + 1) * len(list1) / 40])))
    for i in threads:
        i.start()
        time.sleep(2)
    for i in threads:
        i.join()
        time.sleep(2)

def pagecode(l):
    # driver = webdriver.Chrome()
    l1 = []
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
    print l1


def start():
    thread(getIp())
    # pagecode(getIpnull())



start()


#timeStamp('18-01-22 06:44')
