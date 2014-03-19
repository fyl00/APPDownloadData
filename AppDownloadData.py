# -*- coding: utf-8 -*-
#---------------------------------------  
#   Name：AppDownloadData
#   VER：0.1  
#   Author：FryeLee  
#---------------------------------------


import urllib2
import sys
import json
import re
from bs4 import BeautifulSoup

appname=raw_input(">>>>>请输入你想要查询的APP名字： \n")
#解决url中文编码问题
appname = appname.decode(sys.stdin.encoding).encode("utf-8")
data_DL={'platform':'','data':''}
#保存搜索结果所有序号
choice_list =[]
#保存当前平台的数据
data_DL_list=[]

#输出搜索结果
def printlist(list):
    if list:
        print '>>>>>在'+data_DL['platform']+'中搜索结果如下：'
        if len(list) == 1:
            print '1: %s;'%(list[0])
        else:
            for i in range(0,len(list)-1):
                print '%s：%s;'%(i,list[i]),

#将搜索结果转为数字列表
def liststr(list):
    for i in range(0,len(list)-1):
        choice_list.append(str(i))
    return choice_list

#---------------------------------------
#豌豆荚数据
#---------------------------------------
data_DL['platform']='豌豆荚'

#豌豆荚搜索结果
def WDJsearch(appname):
    link = 'http://apps.wandoujia.com/api/v1/search/' +appname + '?max=12&hasAd=0&start=0&opt_fields=,title,packageName,installedCountStr'
    search_result = urllib2.urlopen(link).read()
    #print search_result
    search_result_json = json.loads(search_result)
    app_list=[]
    WDJdatajudge(appname,search_result_json,app_list)

#判断搜索结果是不是不存在，存在的话是不是和第一个数据的title相同
def WDJdatajudge(appname,result,app_list):
    if result['appList']:
        for i in range(0,len(result['appList'])-1):
            title=result['appList'][i]['title'].replace('<em>','')
            title=title.replace('</em>','').encode("utf-8")
            #print title
            if appname == title:
                data_DL['data'] = result['appList'][i]['installedCountStr'].encode("utf-8")
                print '（%s 在豌豆荚上的下载量为 %s）' %(title,data_DL['data'])
                app_list=False
                break
            else:
                app_list.append(title)
    else:
        appname=raw_input(">>>>>在"+data_DL['platform']+"中未找到你所要查询的APP的数据，请重新输入你想要查询的APP名字： \n")
        WDJsearch(appname)
    WDJadvancedsearch(app_list,result)

#执行搜索函数

#如果搜索结果中没有和用户输入的名称完全一致的程序，那么让用户选择
def WDJadvancedsearch(list,result):
    while list:
        printlist(list)
        user_choice= raw_input('\n>>>>>请输入你所要查询的APP序号（如果没有你想查询的APP，请输入re）：\n')
        liststr(list)
        if (user_choice == 're') or (user_choice in choice_list):
            if user_choice in choice_list:
                user_choice = int(user_choice)
                data_DL['data']=result['appList'][user_choice]['installedCountStr'].encode("utf-8")
                print '（%s 在豌豆荚上的下载量为 %s）' %(list[user_choice],data_DL['data'])
                list=False
            else:
                appname=raw_input(">>>>>请重新输入你想要查询的APP名字： \n")
                appname = appname.decode(sys.stdin.encoding).encode("utf-8")
                WDJsearch(appname)
                list=False
        else:
            print '>>>>>输入错误'

WDJsearch(appname)
#将当前平台的数据暂时保存
data_DL_list.append(data_DL.copy())

#---------------------------------------
#应用宝数据
#---------------------------------------
data_DL['platform']='应用宝'

#搜索结果中没有和用户输入的名称完全一致的程序，那么让用户选择
def YYBadvancedsearch(list,result):
    while list:
        printlist(list)
        user_choice= raw_input('\n>>>>>请输入你所要查询的APP序号（如果没有你想查询的APP，请输入re）：\n')
        liststr(list)
        if (user_choice == 're') or (user_choice in choice_list) :
            if user_choice in choice_list:
                user_choice = int(user_choice)
                data_DL['data'] = result['info']['value'][int(user_choice)]['downcount'].encode("utf-8")
                print '（%s 在应用宝上的下载量为 %s）' %(list[user_choice],data_DL['data'])
                list=False
            else:
                appname=raw_input(">>>>>请重新输入你想要查询的APP名字： \n")
                appname = appname.decode(sys.stdin.encoding).encode("utf-8")
                YYBsearch(appname)
                list=False
        else:
            print '>>>>>输入错误'

#判断搜索结果是不是不存在
def searchresultjudge(appname,result,app_list):
    if result['info']:
        for i in range(0,len(result['info']['value'])-1):
            title_search_result=result['info']['value'][i]['softname'].encode("utf-8")
            #print title_search_result
            #print len(title_search_result)
            if appname == title_search_result:
                data_DL['data'] = result['info']['value'][i]['downcount'].encode("utf-8")
                print '（%s 在应用宝上的下载量为 %s）' %(appname,data_DL['data'])
                break
            else:
                app_list.append(title_search_result)
    else:
        appname=raw_input(">>>>>在"+data_DL['platform']+"中未找到你所要查询的APP的数据，请重新输入你想要查询的APP名字： \n")
        YYBsearch(appname)

#搜索所要查询的APP
def YYBsearch(appname):
    link = 'http://android.myapp.com/android/qrysearchrslt_web?actiondetail=0&softname=' +appname + '&pageNo=1&pageIndex=-1&pageSize=10'
    search_result = urllib2.urlopen(link).read()
    #print search_result
    search_result_json = json.loads(search_result)
    app_list=[]
    searchresultjudge(appname,search_result_json,app_list)
    YYBadvancedsearch(app_list,search_result_json)

YYBsearch(appname)

#print data_DL
#将当前平台的数据暂时保存
data_DL_list.append(data_DL.copy())

#---------------------------------------
#360手机助手数据
#---------------------------------------
data_DL['platform']='360手机助手'
app_list=[]

#搜索结果中没有和用户输入的名称完全一致的程序，那么让用户选择
def QHadvancedsearch(list,result):
    while list:
        printlist(list)
        user_choice= raw_input('\n>>>>>请输入你所要查询的APP序号（如果没有你想查询的APP，请输入re）：\n')
        liststr(list)
        if (user_choice == 're') or (user_choice in choice_list) :
            if user_choice in choice_list:
                user_choice = int(user_choice)
                apprename = list[user_choice]
                downloadsoup=result.find(attrs={'class':'SeaCon'}).find(attrs={'title':apprename}).parent.parent.parent.parent
                download_data=downloadsoup.find(attrs={'class':'downNum'}).next_element.encode('utf-8')
                download_data=re.search(r'(?P<down_num>\d*)\D*',download_data)
                #print download_data
                data_DL['data']=download_data.group('down_num')
                print '（%s 在360手机助手的下载量为 %s）'%(apprename,data_DL['data'])
                list=False
            else:
                appname=raw_input(">>>>>请重新输入你想要查询的APP名字： \n")
                appname = appname.decode(sys.stdin.encoding).encode("utf-8")
                QHsearch(appname)
                list =False
        else:
            print '>>>>>输入错误'

#判断第一个搜索结果是否为所需结果
def QHsearchjudge(appname,soup,result,list):
    if result:
        firstapp=re.search(r'title="(?P<mt>\S*)">',str(result[0]))
        firstapp=firstapp.group('mt')
        if appname == firstapp:
            downloadsoup=soup.find(attrs={'class':'SeaCon'}).find('li')
            download_data=downloadsoup.find(attrs={'class':'downNum'}).next_element.encode('utf-8')
            #将数据放到保存
            download_data=re.search(r'(?P<down_num>\d*)\D*',download_data)
            data_DL['data']=download_data.group('down_num')
            print '（%s 在360手机助手的下载量为 %s） '%(appname,data_DL['data'])

        else:
            #获得所有搜寻结果
            for data in result:
                title=re.search(r'title="(?P<mt>\S*)">',str(data))
                #print title.group('mt')
                list.append(title.group('mt'))
    else:
        appname=raw_input(">>>>>在"+data_DL['platform']+"中未找到你所要查询的APP的数据，请重新输入你想要查询的APP名字： \n")
        QHsearch(appname)

#搜索所要查询的APP
def QHsearch(appname):
    link='http://zhushou.360.cn/search/index/?kw='+appname
    html=urllib2.urlopen(link).read()
    websoup=BeautifulSoup(html)
    search_data=websoup.find(attrs={'class':'SeaCon'}).find_all('h3')
    #print search_data
    app_list=[]
    QHsearchjudge(appname,websoup,search_data,app_list)
    QHadvancedsearch(app_list,websoup)

QHsearch(appname)
data_DL_list.append(data_DL.copy())

#---------------------------------------
#91手机助手
#---------------------------------------
data_DL['platform']='91手机助手'
app_list=[]

#搜索结果中没有和用户输入的名称完全一致的程序，那么让用户选择
def NINEONEadvancesearch(list,soup):
    while list is not None:
        printlist(list)
        user_choice= raw_input('\n>>>>>请输入你所要查询的APP序号（如果没有你想查询的APP，请输入re）：\n')
        liststr(list)
        if (user_choice == 're') or (user_choice in choice_list):
            if user_choice in choice_list:
                user_choice = int(user_choice)
                apprename = list[user_choice]
                linkdata = soup.find(attrs={'class':'search-list'}).find('a',text=apprename)
                NINEONEpage(str(linkdata),apprename)
                list=None
            else:
                appname=raw_input("请重新输入你想要查询的APP名字 \n")
                appname = appname.decode(sys.stdin.encoding).encode("utf-8")
                NINEONEsearch(appname)
                list=None
        else:
            print '>>>>>输入错误 \n'

#91APP页函数
def NINEONEpage(data,appname):
    pagelink=re.search(r'href="(?P<plink>\S*)">',data)
    pagelink = pagelink.group('plink')
    pagelink = 'http://apk.91.com'+pagelink
    downloadsoup=BeautifulSoup(urllib2.urlopen(pagelink).read())
    download_data=downloadsoup.find(attrs={'class':'s_intro_txt'}).encode('utf-8')
    #将数据放到保存
    download_data=re.search(r'下载次数：(?P<down_num>\S*)</li>*',download_data)
    data_DL['data']=download_data.group('down_num')
    print '（%s 在91手机助手的下载量为 %s）'%(appname,data_DL['data'])

#91搜索页结果函数
def NINEONEsearch(appname):
    link='http://apk.91.com/Soft/Android/search/1_0_0_0_'+appname
    #print link
    html=urllib2.urlopen(link).read()
    websoup=BeautifulSoup(html)
    app_list=[]
    search_list = websoup.find(attrs={'class':'search-list'})
    if search_list:
        search_data=websoup.find(attrs={'class':'search-list'}).find_all('h4')
        firstapp=re.search(r'html">(?P<mt>\S.*)</a>',str(search_data[0]))
        firstapp=firstapp.group('mt')
        #print firstapp
        if appname == firstapp:
            NINEONEpage(str(search_data[0]),appname)
        else:
            #获得所有搜寻结果
            for data in search_data:
                #print data
                title=re.search(r'html">(?P<mt>\S.*)</a>',str(data))
                app_list.append(title.group('mt'))
        NINEONEadvancesearch(app_list,websoup)
    else:
        appname=raw_input(">>>>>在"+data_DL['platform']+"中未找到你所要查询的APP的数据，请重新输入你想要查询的APP名字： \n")
        NINEONEsearch(appname)


NINEONEsearch(appname)
data_DL_list.append(data_DL.copy())

#---------------------------------------
#百度手机助手数据
#---------------------------------------
data_DL['platform']='百度手机助手'

def BDsearch(appname):
    link='http://m.baidu.com/s?st=10a001&tn=webmkt&pre=web_am_index&word='+appname
    html=urllib2.urlopen(link).read()
    websoup=BeautifulSoup(html)
    app_list = []
    search_list=websoup.find(attrs={'class':'dataList'})
    if search_list:
        search_data=websoup.find(attrs={'class':'dataList'}).find_all('h4')
        #print search_data
        #判断第一个搜索结果是否为所需结果
        firstapp=websoup.find(attrs={'class':'dataList'}).find('h4').get_text().encode("utf-8")
        if appname == firstapp:
            download_data=websoup.find(attrs={'class':'dataList'}).find(attrs={'class':'date'}).encode('utf-8')
            #将数据放到保存
            download_data=re.search(r'下载次数：(?P<down_num>\S*)</span>',download_data)
            data_DL['data']=download_data.group('down_num')
            print '（%s 在百度手机助手的下载量为 %s）'%(appname,data_DL['data'])
            app_list = None
        else:
            #获得所有搜寻结果
            for data in search_data:
                #print data
                title=re.search(r'<h4>(?P<mt>[^<]*)<',str(data))
                #print title
                app_list.append(title.group('mt'))
        while app_list:
            printlist(app_list)
            user_choice= raw_input('\n>>>>>请输入你所要查询的APP序号（如果没有你想查询的APP，请输入re）：\n')
            liststr(app_list)
            if (user_choice == 're') or (user_choice in choice_list) :
                if user_choice in choice_list:
                    user_choice = int(user_choice)
                    apprename = app_list[user_choice]
                    search_data=websoup.find(attrs={'class':'dataList'}).find_all('li')
                    for data in search_data:
                        #虽然在编码之后的显示情况下，data字符串中是含有appname的
                        #但是两者的编码方式似乎不同，所以转换成unicode之后再进行判断
                        #当明确知道两者有包含关系时，但未按预期执行时，可以用repr判断编码方式是否相同
                        if apprename.decode(sys.stdin.encoding) in str(data).decode(sys.stdin.encoding):
                            download_data=re.search(r'下载次数：(?P<down_num>\S*)</span>',str(data))
                            #print download_data
                            data_DL['data']=download_data.group('down_num')
                            print '（%s 在百度手机助手的下载量为 %s）'%(apprename,data_DL['data'])
                            app_list=None
                            break
                else:
                    appname=raw_input(">>>>>请重新输入你想要查询的APP名字： \n")
                    appname = appname.decode(sys.stdin.encoding).encode("utf-8")
                    BDsearch(appname)
            else:
                print '>>>>>输入错误\n'
    else:
        appname=raw_input(">>>>>在"+data_DL['platform']+"中未找到你所要查询的APP的数据，请重新输入你想要查询的APP名字： \n")
        BDsearch(appname)

BDsearch(appname)
data_DL_list.append(data_DL.copy())
#总结数据
print'----------------\n%s的数据如下：'%appname
for data in data_DL_list:
    print '在 %s 的下载量为 %s'%(data['platform'],data['data'])

