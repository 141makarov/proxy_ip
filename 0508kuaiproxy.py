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

def getpage(url1,i):
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'Connection': 'keep-alive',
               'Content-Type': 'application/json; charset=UTF-8',
               'Cookie': 'MxVisitorUID=d797041e-bdc6-462c-a41c-4023d4d8fc74; _vis_opt_exp_312_exclude=1; _vwo_uuid=974491D5B9066661CAAE036DBFB5984E; _vis_opt_exp_335_combi=2; _vis_opt_s=2%7C; _ceg.s=ov46sb; _ceg.u=ov46sb; _gat=1; ismobile=false; _cio=aa8504a9-17c9-86fd-7dfb-eb0cbc5df5a4; _ga=GA1.2.636406067.1501461605; _gid=GA1.2.21041308.1507970087; ki_t=1501461610219%3B1507970091131%3B1507970111250%3B12%3B81; ki_r=; _vwo_uuid_v2=974491D5B9066661CAAE036DBFB5984E|782ec007ad63acefe56b46a7f7b32ad7; _mx_u={"UserId":"00000000-0000-0000-0000-000000000000","UserName":null,"FirstName":null,"IsAdmin":false,"IsPaidUser":false,"IsLoggedIn":false,"MxVisitorUid":"d797041e-bdc6-462c-a41c-4023d4d8fc74","AppUID":"2eab821e-fdad-4545-9730-d2ce7e6ccb3e"}; _gaexp=GAX1.2.jQWr1JWLTCOH_ZPj74b2mA.17514.1!3jEbJbKJQM6-_lqmJEDxKw.17517.2!fUhZDJh2SvymWf4W_nFisQ.17544.1; _mx_vtc=AB-177=Variation&AB-175=Variation&AB-197B=Variation&AB-166=Variation&AB-205=Control&VWO-Blocked=true&AB-226=Control&AB-240=Control&AB-216=Control&AB-229=variation&AB-230=Control',
               'Host': 'mxtoolbox.com',
               'MasterTempAuthorization': '2eab821e-fdad-4545-9730-d2ce7e6ccb3e',
               'Origin': 'https://mxtoolbox.com',
               'Referer': 'https://mxtoolbox.com/SuperTool.aspx?action=blacklist%3a98.126.12.45&run=toolpage',
               'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    proxies = {
        "http": None,
        "https": None,
    }
    url = url1 +"/"+ str(i)
    print 'the url:',url
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}

    # r = requests.get(url, proxies=proxies,headers = headers)
    '''session = requests.Session()
    session.trust_env = False
    r = session.get(url, headers=headers)
    url = 'http://www.xicidaili.com/nn/' + str(i)'''
    # req = urllib2.Request(url, headers=header)'''
    '''proxy_handler = urllib2.ProxyHandler({'http':None,"https": None})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)
    res = urllib2.urlopen(url).read()'''

    var_proxyswitch = True

    res = requests.get(url, proxies=proxies,headers = headers)
    # print res.text.encode('utf-8')
    return res.text

def insertMysql(list):
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute(sql_insertq, list)
    cur.close()
    conn.commit()
    conn.close()


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
def timeStamp(data):
    timeArray = time.strptime(data, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    # print timeStamp
    return timeStamp

def interRegional(now, first, last):
    if first - now >= 0 and now - last > 0:
        return True
    else:
        return False

def timeStampnow(data):
    timeArray = time.strptime(data, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def judgePage(url_list):
    l1 = getIp()
    dict1 = {'ip': '', 'proxy': '', 'add': '', 'unname': '', 'type': '', 'speed': '', 'connecttime': '',
             'alivedays': '', 'testdays': '1'}


    for url in url_list:
        page = 1
        print 'finding url:',url
        while True:
            pagesoure = getpage(url,page)
            soup = BeautifulSoup(pagesoure, 'lxml')
            time.sleep(2)
            tr = soup.find_all("tr")  # <table class="table table-striped table-bordered">
            for i in range(1, len(tr)):
                td = tr[i].find_all('td')
                now = timeStampnow(td[6].text[:10])
                print td[6].text[:10]
                last = timeStamp(str(datetime.date.today() - datetime.timedelta(days=2)))  # 至当前日期减y天1378
                first = timeStamp(str(datetime.date.today() - datetime.timedelta(days=1)))  # 从当前日期减x天
                if interRegional(now, first, last) == True:
                    dict1['ip'] = td[0].text
                    dict1['proxy'] = td[1].text
                    dict1['unname'] = td[2].text
                    dict1['type'] = td[3].text
                    dict1['add'] = td[4].text
                    dict1['speed'] = td[5].text

                    dict1['source'] = 'kuaidaili'
                    # print dict1['ip']
                    if dict1['ip'] not in l1:
                        print dict1
                        # insertMysql(dict1)
            if compareTime(last, now) == False:
                print 'last page data', td[6].text
                break
            else:
                page += 1

def compareTime(record, now):
    if now - record > 0:
        return True
    else:
        return False

def start():
    url_list1 = ['https://www.kuaidaili.com/free/intr','https://www.kuaidaili.com/free/inha']
    judgePage(url_list1)

if __name__ == "__main__":
    start()