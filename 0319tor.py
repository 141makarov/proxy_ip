# coding=utf-8
# 爬取http://www.blutmagie.de 及相关whois和Router Detail，功能爬取插入数据库，当无法访问路由器信息则跳过，直接访问whois插入，如果都不能访问就直接插入数据库，不使用代理直接request法，参考https://stackoverflow.com/questions/28521535/requests-how-to-disable-bypass-proxy 修改时间2018/4/1
from datetime import datetime
import sys
import io
import urllib2
import time
from bs4 import BeautifulSoup
import mysql.connector
import threading
import socket
import requests
import re
global url
url = 'http://www.blutmagie.de/'
sql_insert1 = "insert into torinfo0323(OnionRouterPort,CountryCode,mlon,mlat,RouterName,bandwidth,uptime,Hostname,IPAddress,otherinfo,orport,dirport,badexit,firstseen,asname,asnumber,consensusbandwidth,oraddress,Contact,Fingerprint,DirectoryServerPort,Family,inetnum,netname,descr,adminc,techc,mntby,source,parent,person,address,phone,nichdl,Platform_Version,LastDescriptorPublished,BandwidthObservedInBps,status)values( %(OnionRouterPort)s,%(CountryCode)s,%(mlon)s,%(mlat)s,%(RouterName)s,%(bandwidth)s,%(uptime)s,%(Hostname)s,%(IPAddress)s,%(otherinfo)s,%(orport)s,%(dirport)s,%(badexit)s,%(firstseen)s,%(asname)s,%(asnumber)s,%(consensusbandwidth)s,%(oraddress)s,%(Contact)s,%(Fingerprint)s,%(DirectoryServerPort)s,%(Family)s,%(inetnum)s,%(netname)s,%(descr)s,%(admin-c)s,%(tech-c)s,%(mnt-by)s,%(source)s,%(parent)s,%(person)s,%(address)s,%(phone)s,%(nic-hdl)s,%(PlatformVersion)s,%(LastDescriptorPublished)s,%(BandwidthInBps)s,%(status)s)"

config = {'host': '127.0.0.1',
          'user': 'root',
          'password': '123456',
          'port': 3306,
          'database': 'mydata',
          'charset': 'utf8'}

def country_states():
    fp = open("C:\Users\mxf\PycharmProjects\untitled\country abbreviation.txt", 'r+')
    record = fp.read()
    fp.close()
    c =  record.replace(' ','')
    #print c
    dict1 = {}
    for i in c.split('\n'):
        # print i.split(':')
        key = i.split(':')[0]
        value = i.split(':')[1]
        dict1[key] = value

    # print dict1
    return dict1


def getpage(url):
    socket.setdefaulttimeout(10)
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
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    # import requests

    # session = requests.Session()
    # session.trust_env = False
    # response = session.get(url, headers=headers)
    # print response.text .encode('GBK','ignore').decode('GBk')

    # r = requests.get(url, headers=headers)
    # print r.text.decode('utf-8')

    # print 'http://www.blocklist.de/en/search.html?ip='+str(ip)+'&action=search&send=start+search'
    done = 1
    while done >= 0:
        try:
            session = requests.Session()
            session.trust_env = False

            r = session.get(url, headers=headers)
            # r = requests.get(url, headers=headers)
            done = 0
            # print r.text
            return r.text.encode('GBK','ignore').decode('GBk')

            # return res.read()
        except:
            done -= 1

            print  'last unjudge times', done
            continue

def insertMysqlip(sql_insert,list):
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute(sql_insert, list)
    cur.close()
    conn.commit()
    conn.close()

def updatatimeMysql(list):
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute('update torinfo0323 set updatatime=SYSDATE() where IPAddress = "%s"', list)
    cur.close()
    conn.commit()
    conn.close()

def getIp():
    conn = mysql.connector.connect(**config)
    cur = conn.cursor()
    cur.execute("select IPAddress from torinfo0323" )
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

def judgeMainpage(pagesoure):
    dict1 = {'OnionRouterPort': '', 'CountryCode': '', 'mlon': '', 'mlat': '', 'RouterName': '', 'bandwidth': '',
             'uptime': '', 'Hostname': '', 'IPAddress': '', 'otherinfo': '', 'orport': '', 'dirport': '', 'badexit': '',
             'firstseen': '', 'asname': '', 'asnumber': '', 'consensusbandwidth': '', 'oraddress': '', 'Contact': '',
             'Fingerprint': '',  'DirectoryServerPort': '', 'Platform/Version': '',
             'LastDescriptorPublished(GMT)': '', 'CurrentUptime': '', 'Bandwidth(Max/Burst/Observed-InBps)': '',
             'Family': '', 'inetnum': '', 'netname': '', 'descr': '', 'admin-c': '', 'tech-c': '', 'status': '',
             'mnt-by': '', 'source': '', 'parent': '', 'person': '', 'address': '', 'phone': '', 'nic-hdl': ''}

    soup = BeautifulSoup(pagesoure, 'lxml')
    tbody = soup.find(class_="displayTable")
    tr = tbody.find_all('tr', class_='r')
    sqlip = getIp()
    updatacount = 0
    for i in range(1, len(tr)):
        td = tr[i].find_all('td')
        routerUrl = tr[i].find_all('a')[1]['href']#router detail
        whoisUrl = tr[i].find(class_='iT').find('a')['href']
        ip = re.compile(r'\d+.\d+.\d+.\d+').findall(whoisUrl)[0]
        if ip in sqlip:
            print ip,'has in sql'
            updatatimeMysql(ip)
            continue
        else:
            updatacount += 1
            dict1['mlat'] = re.compile('mlat=(.*?)&').findall(td[0].find('a')['href'])[0]  # mlat
            dict1['mlon'] = re.compile('mlon=(.*?)&').findall(td[0].find('a')['href'])[0]  # mlon
            dict1['Router Name'] = td[0].text
            dict1['bandwidth'] = td[1].text
            dict1['uptime'] = td[4].text
            tdit = td[5].find_all('td')
            otherinfo = []
            s = ''
            for i in range(1, len(tdit)):
                otherinfo.append(tdit[i].find('img')['title'])
            for j in otherinfo:
                s += str(j) + ','
            dict1['otherinfo'] = s
            dict1['orport'] = td[7 + len(otherinfo)].text
            dict1['dirport'] = td[8 + len(otherinfo)].text
            dict1['firstseen'] = td[10 + len(otherinfo)].text
            dict1['asname'] = td[11 + len(otherinfo)].text
            dict1['asnumber'] = td[12 + len(otherinfo)].text
            if tr[1].find(class_='F0'):
                dict1['badexit'] = 0;
            else:
                dict1['badexit'] = 1
            dict1['consensusbandwidth'] = td[13 + len(otherinfo)].text
            print 'main'
            try:
                judgeRouterDetail(dict1,routerUrl,whoisUrl)
            except:
                print 'no router detail'
                try:
                    judgeWhois(dict1,whoisUrl)
                except:
                    print 'no whois'
                    dict2 = dealdict(dict1)
                    # insertMysqlip(sql_insert1, dict2)
                    continue
    print 'new updata count:',updatacount

def judgeRouterDetail(dict1,rouUrl,whoisUrl):
    global url

    soup = BeautifulSoup(getpage(url+rouUrl), 'lxml')
    classt = soup.find(class_='TDBLACK')
    tr = classt.find_all('tr')
    for i in range(1, len(tr)):
        try:
            if dict1.has_key((tr[i].text.split(':', 1))[0].replace('\n', '').replace(' ', '')):
                dict1[(tr[i].text.split(':', 1))[0].replace('\n', '').replace(' ', '')] = (tr[i].text.split(':', 1))[1].replace('\n', '')
            else:continue
        except:
            continue
    print  'router detail'
    try:
        judgeWhois(dict1,whoisUrl)
    except:
        print 'no whois'
        dict2 = dealdict(dict1)
        insertMysqlip(sql_insert1, dict2)

def judgeWhois(dict1,whoisUrl):
    global url
    soup = BeautifulSoup(getpage(url+whoisUrl), 'lxml')
    try:
        classt = soup.find(class_='TDBLACK')
        for i in classt.text.split('\n'):
            try:
                if dict1.has_key(i.split(':')[0].replace(' ', '')):
                    dict1[i.split(':')[0].replace(' ', '')] = i.split(':')[1].replace(' ', '')
                else:
                    continue
            except:
                continue
    except:
        print 'no whois'
    print 'whois'
    dict2 = dealdict(dict1)
    insertMysqlip(sql_insert1, dict2)

def dealdict(dict1):
    dict3 = country_states()
    country = dict1['CountryCode'].lower()
    if dict3.has_key(country):
        dict1['CountryCode'] = dict3[country]
    #更改key值方便插入sql
    try:
        dict1['PlatformVersion'] = dict1.pop('Platform/Version')
        dict1['LastDescriptorPublished'] = dict1.pop('LastDescriptorPublished(GMT)')
        dict1['BandwidthInBps'] = dict1.pop('Bandwidth(Max/Burst/Observed-InBps)')
    except:
        print dict1
    return dict1


def start():
    judgeMainpage(getpage(url))

start()
# getpage(url)
# dict1 = {'Hostname': u'cry.ip-eend.nl', 'OnionRouterPort': u'9003', 'bandwidth': u'\xa0\xa024936', 'LastDescriptorPublished': u'2018-03-26 02:43:34', 'source': u'RIPE', 'inetnum': u'192.42.115.0-192.42.115.255', 'Fingerprint': u'B204 DE75 B370 64EF 6A4C 6BAF 955C 5724 578D 0B32 ', 'IPAddress': u'192.42.115.101', 'firstseen': u'2015-04-22\xa0', 'otherinfo': 'Fast Server,Directory Server,Guard Server,Stable Server,Tor 0.3.2.9 on Linux,', 'nic-hdl': u'WB311-RIPE', 'mlat': '52.3824', 'phone': u'+31887873000', 'tech-c': u'WB311-RIPE', 'asnumber': u'1103\xa0', 'Family': u'$6DFEB41C04CCE846871338E85DD5ACF5CFB6C1DD$D665C959571041972EA8C0DD77559EF5579BA112', 'asname': u'SURFNET-NL SURFnet, The Netherlands, NL\xa0', 'PlatformVersion': u'Tor 0.3.1.9 on Linux', 'oraddress': '', 'orport': u'9003', 'netname': u'SURFwim', 'mnt-by': u'AS1103-MNT', 'admin-c': u'WB311-RIPE', 'mlon': '4.8995', 'uptime': u'23 d', 'parent': '', 'descr': u'SURFNET-IP', 'dirport': u'8080', 'DirectoryServerPort': u'8080', 'Router Name': u'\xa0cry', 'RouterName': u'cry', 'badexit': 0, 'consensusbandwidth': u'90900\xa0', 'Contact': u'Gijs Rijnders (tor AT ip-eend DOT nl)', 'address': u'TheNetherlands', 'CountryCode': 'netherlands', 'person': u'WimBiemolt', 'status': u'LEGACY', 'BandwidthInBps': u'1073741824\xa0/\xa01073741824\xa0/\xa043876372', 'CurrentUptime': u'23 Day(s), 16 Hour(s), 19 Minute(s), 15 Second(s)'}
# insertMysqlip(sql_insert1, dict1)
# updatatimeMysql('178.32.181.96')