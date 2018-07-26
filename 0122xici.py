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
    url = url1 + str(i)
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
    # print res.text
    return res.text



def judgePage(url_list):
    dict1 = {'ip': '', 'proxy': '', 'add': '', 'unname': '', 'type': '', 'speed': '', 'connecttime': '',
             'alivedays': '','testdays':'1','source':'xici'}
    page = 1
    list1 = []

    count = 1
    for url in url_list:
        print 'finding url:',url
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

def getIpnull():
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("select ip,proxy from proxy_ip1_text where testdays is NULL" )
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
    for i in range(0,len(list1)):
        print 'last',len(list1)-i,'unjudge'

        if validateIp(list1[i]) == True:
            updateSql(list1[i].split(':')[0])
            print 'succeed',list1[i].split(':')[0]
        else:
            print 'fall',list1[i]
            badSql(list1[i].split(':')[0])

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
    #list1 = [u'180.121.141.227:26625', u'49.70.32.249:47137', u'180.122.144.50:41017', u'106.46.3.187:47691', u'115.221.120.137:25256', u'27.153.128.133:22354', u'49.74.130.150:8123', u'49.89.86.105:37727', u'114.231.155.206:25494']
    threads.append(threading.Thread(target=ipjudge, args=(list1[0:len(list1)/20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[len(list1) / 20:2 * len(list1) / 20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[2 * len(list1) / 20:3 * len(list1) / 20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[3 * len(list1) / 20:4 * len(list1) / 20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[4 * len(list1) / 20:5 * len(list1) / 20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[5 * len(list1) / 20:6 * len(list1) / 20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[6 * len(list1) / 20:7 * len(list1) / 20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[7 * len(list1) / 20:8 * len(list1) / 20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[8 * len(list1) / 20:9 * len(list1) / 20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[9 * len(list1) / 20:10 * len(list1) / 20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[10 * len(list1) / 20:11 * len(list1) / 20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[11 * len(list1) / 20:12 * len(list1) / 20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[12 * len(list1) / 20:13 * len(list1) / 20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[13 * len(list1) / 20:14 * len(list1) / 20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[14 * len(list1) / 20:15 * len(list1) / 20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[15 * len(list1) / 20:16 * len(list1) / 20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[16 * len(list1) / 20:17 * len(list1) / 20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[17 * len(list1) / 20:18 * len(list1) / 20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[18 * len(list1) / 20:19 * len(list1) / 20])))
    threads.append(threading.Thread(target=ipjudge, args=(list1[19 * len(list1) / 20:20 * len(list1) / 20])))
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
def start():
    url_list1 = ['http://www.xicidaili.com/nt/','http://www.xicidaili.com/nn/']
    url_list2 = [ 'http://www.xicidaili.com/wt/','http://www.xicidaili.com/wn/']
    print '正在获取更新的ip'
    judgePage(url_list1)
    judgePage(url_list2)
    # print 'judging database ip'
    # thread(getIp( ))
    # print '正在判断遗漏ip信息'
    # thread(getIpnull())
    # print getIpnull()
    # ipjudgenull(getIp())
    #validateIp('139.196.182.176:808')
start()
# getpage('http://www.xicidaili.com/nt/',1)
#timeStamp('18-01-22 06:44')
# getIp()