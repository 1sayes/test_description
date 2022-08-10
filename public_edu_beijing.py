import requests
import urllib
import pandas as pd
from lxml import etree
import numpy as np
from mysql_util import Mysqldb

# 请求头：用于python伪装成浏览器访问网页
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

# 获取html函数
def gethtml(url):
    try:
        # 访问网站并获取响应
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=15)
        html = response.read().decode('UTF-8', errors='ignore')
        return html
    except Exception as e:
        print("网页{}爬取失败", format(url), "原因", e)

# 获取网页中的文章
def getthml_text(url):
    # 调用获取html响应函数获取网页响应
    res = gethtml(url)
    list = etree.HTML(res)
    try:
        # 通过xpath筛选出所需要的文章内容
        namelist = list.xpath("//div[@class='lh_lists']//a//text()")
        linklist = list.xpath("//div[@class='lh_lists']//a/@href")
        return namelist,linklist
    except Exception as e:
        print('文章爬取失败', "原因", e)

# 通过xpath筛选网页信息
def filter_html(res,xpathstr):
    list1 = etree.HTML(res)
    try:
        # 通过xpath筛选出所需要的网页内容
        result = list1.xpath(xpathstr)
        return result
    except Exception as e:
        print('文章爬取失败', "原因", e)

# 主程序
print('###### 中公教育北京板块信息 ######')
print('栏目名称和连接')
url = 'https://www.offcn.com/bjgwy/kaoshi/1.html'
classlist = getthml_text(url)
namelist = classlist[0]
namelist_x = []
for name in namelist:
    if name != '|':
        namelist_x.append(name)
print(namelist_x)
linklist = []
for link in classlist[1]:
    link = 'https:' + link
    linklist.append(link)
print(linklist)

# 爬取需要的栏目信息
for i in range(len(namelist_x)):
    name = namelist_x[i]
    link = linklist[i]
    # 爬考试公告板块
    if name == '考试公告':
        print('#########考试公告爬取成功#########')
        # 筛选出热门推荐的文章和连接
        titlexpath = "//ul[@class='lh_newBobotm01']/li/a//text()"
        urlxpath = "//ul[@class='lh_newBobotm01']/li/a/@href"
        res = gethtml(link)
        titlelist = filter_html(res, titlexpath)
        urllist = filter_html(res, urlxpath)
        urllist_x = []
        for link in urllist:
            link = 'https:' + link
            urllist_x.append(link)

        # 爬取第一篇公告的内容
        res = gethtml(urllist_x[0])
        notice_table_xpath = "//li/a/b/text()"
        notice_table = filter_html(res, notice_table_xpath)
        notice_tablev = []
        for table in notice_table:
            notice_tablev_xpath = f"//b[./text()='{table}']/following::text()[1]"
            tablev = filter_html(res, notice_tablev_xpath)
            tablev = tablev[0].strip()
            notice_tablev.append(tablev)
        notice_essay_xpath = "//div[@class='offcn_shocont']/p//text()"
        notice_essay_1 = filter_html(res, notice_essay_xpath)
        notice_essay_1_total = ''
        for j in notice_essay_1:
            notice_essay_1_total += j
        # 爬第一篇公告第二页剩余文章
        notice_url_2 = urllist_x[0][:-5] + '_2' + urllist_x[0][-5:]
        #         print(notice_url_2)
        notice_essay_2_xpath = "//div[@class='offcn_shocont']/p//text()"
        res = gethtml(notice_url_2)
        notice_essay_2 = filter_html(res, notice_essay_2_xpath)
        notice_essay_2_total = ''
        for j in notice_essay_2:
            notice_essay_2_total += j
        notice_essay_total = notice_essay_1_total + notice_essay_2_total

    # 爬取考公时间模块
    if name == '考试时间':
        print('#########考试时间爬取成功#########')
        # 筛选出热门推荐的文章和连接
        res = gethtml(link)
        titlexpath = "//ul[@class='lh_newBobotm01']/li/a//text()"
        urlxpath = "//ul[@class='lh_newBobotm01']/li/a/@href"
        titlelist = filter_html(res, titlexpath)
        urllist = filter_html(res, urlxpath)
        urllist_x = []
        for link in urllist:
            link = 'https:' + link
            urllist_x.append(link)

        # 爬取第一篇考试时间文章的内容
        res = gethtml(urllist_x[0])
        # 爬取文章
        time_essay_xpath = "//div[@class='offcn_shocont']/p/text()"
        time_essay = filter_html(res, time_essay_xpath)
        # 爬取历年时间表
        time_table_xpath = "//table[@border='1']//td//text()"
        time_table = filter_html(res, time_table_xpath)

    if name == '考试大纲':
        print('#########考试大纲爬取成功#########')
        # 筛选出热门推荐的文章和连接
        res = gethtml(link)
        titlexpath = "//ul[@class='lh_newBobotm01']/li/a//text()"
        urlxpath = "//ul[@class='lh_newBobotm01']/li/a/@href"
        titlelist = filter_html(res, titlexpath)
        urllist = filter_html(res, urlxpath)
        #         print(titlelist)
        #         print(urllist)
        urllist_x = []
        for link in urllist:
            link = 'https:' + link
            urllist_x.append(link)

        # 爬取第一篇考试大纲文章的内容
        res = gethtml(urllist_x[0])
        outline_title_xpath = "//div[@class='offcn_shocont']/p/a/text()"
        outline_url_xpath = "//div[@class='offcn_shocont']/p/a/@href"

        outline_title = filter_html(res, outline_title_xpath)
        outline_url = filter_html(res, outline_url_xpath)
        #         print(outline_title)
        #         print(outline_url)

        outline_essay_xpath = "//div[@class='offcn_shocont']/p/text()"
        outline_essay_list = []
        for j in range(len(outline_title)):
            res = gethtml(outline_url[j])
            outline_essay = filter_html(res, outline_essay_xpath)
            outline_essay_total = ''
            for k in outline_essay:
                outline_essay_total += k
            outline_essay_list.append(outline_essay_total)

    if name == '职位表':
        print('#########职位表爬取成功#########')
        # 筛选出热门推荐的文章和连接
        orilink = link
        res = gethtml(link)
        titlexpath = "//ul[@class='lh_newBobotm01']/li/a//text()"
        urlxpath = "//ul[@class='lh_newBobotm01']/li/a/@href"
        hot_post_table = filter_html(res, titlexpath)
        hot_post_table_link = filter_html(res, urlxpath)

        hot_post_table_link_x = []
        for link in hot_post_table_link:
            link = 'https:' + link
            hot_post_table_link_x.append(link)

        # 筛选出5页内的职位表
        page_n = 5
        post_table = []
        post_table_link = []
        titlexpath_li = "//ul[@class='lh_newBobotm02']/li[not(@style)]//a[@title]/text()"
        urlxpath_li = "//ul[@class='lh_newBobotm02']/li[not(@style)]//a[@title]/@href"
        for j in range(page_n):
            page = j + 1
            post_table += filter_html(res, titlexpath_li)
            post_table_link += filter_html(res, urlxpath_li)
            if page >= 2:
                link = orilink[:-5] + f'/{page}.html'
                res = gethtml(link)

        post_table_link_x = []
        for link in post_table_link:
            link = 'https:' + link
            post_table_link_x.append(link)

        #         print(post_table_link_x[1])

        post_table = hot_post_table + post_table
        post_table_link_x = hot_post_table_link_x + post_table_link_x

    if name == '报名人数':
        print('#########报名人数爬取成功#########')
        # 筛选出热门推荐的文章和连接
        orilink = link
        res = gethtml(link)
        titlexpath = "//ul[@class='lh_newBobotm01']/li/a//text()"
        urlxpath = "//ul[@class='lh_newBobotm01']/li/a/@href"
        hot_regi_n = filter_html(res, titlexpath)
        hot_regi_n_link = filter_html(res, urlxpath)

        hot_regi_n_link_x = []
        for link in hot_regi_n_link:
            link = 'https:' + link
            hot_regi_n_link_x.append(link)

        # 筛选出报名人数文章
        titlexpath_li = "//ul[@class='lh_newBobotm02']/li[not(@style)]//a[@title]/text()"
        urlxpath_li = "//ul[@class='lh_newBobotm02']/li[not(@style)]//a[@title]/@href"
        regi_n = filter_html(res, titlexpath_li)
        regi_n_link = filter_html(res, urlxpath_li)

        regi_n_link_x = []
        for link in regi_n_link:
            link = 'https:' + link
            regi_n_link_x.append(link)

        regi_n = hot_regi_n + regi_n
        regi_n_link_x = hot_regi_n_link_x + regi_n_link_x

    if name == '成绩查询':
        print('#########成绩查询爬取成功#########')
        # 筛选出热门推荐的文章和连接
        orilink = link
        res = gethtml(link)
        titlexpath = "//ul[@class='lh_newBobotm01']/li/a//text()"
        urlxpath = "//ul[@class='lh_newBobotm01']/li/a/@href"
        grade = filter_html(res, titlexpath)
        grade_link = filter_html(res, urlxpath)

        grade_link_x = []
        for link in grade_link:
            link = 'https:' + link
            grade_link_x.append(link)

    if name == '分数线':
        print('#########分数线爬取成功#########')
        # 筛选出热门推荐的文章和连接
        orilink = link
        res = gethtml(link)
        titlexpath = "//ul[@class='lh_newBobotm01']/li/a//text()"
        urlxpath = "//ul[@class='lh_newBobotm01']/li/a/@href"
        gradeline = filter_html(res, titlexpath)
        gradeline_link = filter_html(res, urlxpath)

        gradeline_link_x = []
        for link in gradeline_link:
            link = 'https:' + link
            gradeline_link_x.append(link)

        # 爬第一篇和第二篇文章
        # 第一篇 爬文章
        res = gethtml(gradeline_link_x[0])
        gradeline_essay_xpath = "//div[@class='offcn_shocont']/p//text()"
        gradeline_essay = filter_html(res, gradeline_essay_xpath)
        # 第二篇 爬历年分数线表格
        res = gethtml(gradeline_link_x[1])
        gradeline_table_xpath = "//table[@class='biaoge']//td//text()"
        gradeline_table = filter_html(res, gradeline_table_xpath)

    if name == '面试名单':
        print('#########面试名单爬取成功#########')
        # 筛选出热门推荐的文章和连接
        orilink = link
        res = gethtml(link)
        titlexpath = "//ul[@class='lh_newBobotm01']/li/a//text()"
        urlxpath = "//ul[@class='lh_newBobotm01']/li/a/@href"
        hot_interview = filter_html(res, titlexpath)
        hot_interview_link = filter_html(res, urlxpath)

        hot_interview_link_x = []
        for link in hot_interview_link:
            link = 'https:' + link
            hot_interview_link_x.append(link)

        # 筛选出3页内的面试名单
        page_n = 3
        interview = []
        interview_link = []
        titlexpath_li = "//ul[@class='lh_newBobotm02']/li[not(@style)]//a[@title]/text()"
        urlxpath_li = "//ul[@class='lh_newBobotm02']/li[not(@style)]//a[@title]/@href"
        for j in range(page_n):
            page = j + 1
            interview += filter_html(res, titlexpath_li)
            interview_link += filter_html(res, urlxpath_li)
            if page >= 2:
                link = orilink[:-5] + f'/{page}.html'
                res = gethtml(link)

        interview_link_x = []
        for link in interview_link:
            link = 'https:' + link
            interview_link_x.append(link)

        interview = hot_interview + interview
        interview_link_x = hot_interview_link_x + interview_link_x

    if name == '调剂职位':
        print('#########调剂职位爬取成功#########')
        # 筛选出热门推荐的文章和连接
        orilink = link
        res = gethtml(link)
        titlexpath = "//ul[@class='lh_newBobotm01']/li/a//text()"
        urlxpath = "//ul[@class='lh_newBobotm01']/li/a/@href"
        hot_adjust = filter_html(res, titlexpath)
        hot_adjust_link = filter_html(res, urlxpath)

        hot_adjust_link_x = []
        for link in hot_adjust_link:
            link = 'https:' + link
            hot_adjust_link_x.append(link)

        # 筛选出5页内的调剂职位
        page_n = 5
        adjust = []
        adjust_link = []
        titlexpath_li = "//ul[@class='lh_newBobotm02']/li[not(@style)]//a[@title]/text()"
        urlxpath_li = "//ul[@class='lh_newBobotm02']/li[not(@style)]//a[@title]/@href"
        for j in range(page_n):
            page = j + 1
            adjust += filter_html(res, titlexpath_li)
            adjust_link += filter_html(res, urlxpath_li)
            if page >= 2:
                link = orilink[:-5] + f'/{page}.html'
                res = gethtml(link)

        adjust_link_x = []
        for link in adjust_link:
            link = 'https:' + link
            adjust_link_x.append(link)

        adjust = hot_adjust + adjust
        adjust_link_x = hot_adjust_link_x + adjust_link_x

    if name == '录用公示':
        print('#########录用公示爬取成功#########')
        # 筛选出热门推荐的文章和连接
        orilink = link
        res = gethtml(link)
        titlexpath = "//ul[@class='lh_newBobotm01']/li/a//text()"
        urlxpath = "//ul[@class='lh_newBobotm01']/li/a/@href"
        hot_employ = filter_html(res, titlexpath)
        hot_employ_link = filter_html(res, urlxpath)

        hot_employ_link_x = []
        for link in hot_employ_link:
            link = 'https:' + link
            hot_employ_link_x.append(link)

        # 筛选出2页内的录用公示
        page_n = 2
        employ = []
        employ_link = []
        titlexpath_li = "//ul[@class='lh_newBobotm02']/li[not(@style)]//a[@title]/text()"
        urlxpath_li = "//ul[@class='lh_newBobotm02']/li[not(@style)]//a[@title]/@href"
        for j in range(page_n):
            page = j + 1
            employ += filter_html(res, titlexpath_li)
            employ_link += filter_html(res, urlxpath_li)
            if page >= 2:
                link = orilink[:-5] + f'/{page}.html'
                res = gethtml(link)

        employ_link_x = []
        for link in employ_link:
            link = 'https:' + link
            employ_link_x.append(link)

        employ = hot_employ + employ
        employ_link_x = hot_employ_link_x + employ_link_x

    if name == '补录公告':
        print('#########补录公告爬取成功#########')
        # 筛选出热门推荐的文章和连接
        orilink = link
        res = gethtml(link)
        titlexpath = "//ul[@class='lh_newBobotm01']/li/a//text()"
        urlxpath = "//ul[@class='lh_newBobotm01']/li/a/@href"
        hot_collection = filter_html(res, titlexpath)
        hot_collection_link = filter_html(res, urlxpath)

        hot_collection_link_x = []
        for link in hot_collection_link:
            link = 'https:' + link
            hot_collection_link_x.append(link)

    if name == '考试政策':
        print('#########考试政策爬取成功#########')
        # 筛选出热门推荐的文章和连接
        orilink = link
        res = gethtml(link)
        titlexpath = "//ul[@class='lh_newBobotm01']/li/a//text()"
        urlxpath = "//ul[@class='lh_newBobotm01']/li/a/@href"
        hot_policy = filter_html(res, titlexpath)
        hot_policy_link = filter_html(res, urlxpath)

        hot_policy_link_x = []
        for link in hot_policy_link:
            link = 'https:' + link
            hot_policy_link_x.append(link)

        # 筛选出2页内的考试政策
        page_n = 2
        policy = []
        policy_link = []
        titlexpath_li = "//ul[@class='lh_newBobotm02']/li[not(@style)]//a[@title]/text()"
        urlxpath_li = "//ul[@class='lh_newBobotm02']/li[not(@style)]//a[@title]/@href"
        for j in range(page_n):
            page = j + 1
            policy += filter_html(res, titlexpath_li)
            policy_link += filter_html(res, urlxpath_li)
            if page >= 2:
                link = orilink[:-5] + f'/{page}.html'
                res = gethtml(link)

        policy_link_x = []
        for link in policy_link:
            link = 'https:' + link
            policy_link_x.append(link)

        policy = hot_policy + policy
        policy_link_x = hot_policy_link_x + policy_link_x

####### 把爬取到的信息存入数据库之中 #########

# 连接mysql
config = {
    "host": "bj-cynosdbmysql-grp-bzwfkr20.sql.tencentcdb.com",
    "port": 23079,
    "database": "student",
    "charset": "utf8",
    "user": "test",
    "passwd": "Aa123456"
}

mysql = Mysqldb(config)

def printdown(name):
    print(name, '储存完毕')
##### 考试公告数据储存 #####

# 摘要表
# 创建数据表
tablename = '考试公告摘要表'
sql = f"CREATE TABLE {tablename} (id INT AUTO_INCREMENT PRIMARY KEY"
for head in notice_table:
    string = f", {head} VARCHAR(255)"
    sql +=  string
sql += ")"
mysql.create_table(sql)

# 将数据存入表中
id = [1,]
value = tuple(id + notice_tablev)
sql = f"insert into {tablename} values {value}"
mysql.commit_data(sql)

# 公告文章
with open('考试公告.txt', 'w') as f:
    f.write(notice_essay_total)

printdown('考试公告')

#### 考试时间储存 ####

# 考试时间文章
time_essay_total = ''
for i in time_essay:
    time_essay_total += i

with open('考试时间.txt', 'w') as f:
    f.write(time_essay_total)

# 考试时间表

# 创建数据表
tablename = '考试时间表'
sql = f"CREATE TABLE {tablename} (id INT AUTO_INCREMENT PRIMARY KEY"
for head in time_table[:4]:
    string = f", {head} VARCHAR(255)"
    sql += string
sql += ")"
mysql.create_table(sql)

# 将数据存入表中
time_table_np = np.array(time_table[4:]).reshape(len(time_table[4:]) // 4, 4)
id = 1
for value in time_table_np:
    value = tuple(np.insert(value,0,id))
    sql = f"insert into {tablename} values {value}"
    mysql.commit_data(sql)
    id += 1

printdown('考试时间')

#### 考试大纲储存 ####
for i in range(len(outline_title)):
    title = f'{outline_title[i]}.txt'
    with open(title, 'w') as f:
        f.write(outline_essay_list[i])

printdown('考试大纲')

#### 职位表储存 ####

# 创建数据表
tablename = '职位表'
sql = f"CREATE TABLE {tablename} (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), html VARCHAR(255))"
mysql.create_table(sql)

id = 1

for i in range(len(post_table)):
    value = (id, post_table[i], post_table_link_x[i])
    sql = f"insert into {tablename} values {value}"
    mysql.commit_data(sql)
    id += 1

printdown('职位表')

#### 报名人数信息储存 ####
tablename = '报名人数表'
sql = f"CREATE TABLE {tablename} (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), html VARCHAR(255))"
mysql.create_table(sql)

id = 1

for i in range(len(regi_n)):
    value = (id, regi_n[i], regi_n_link_x[i])
    sql = f"insert into {tablename} values {value}"
    mysql.commit_data(sql)
    id += 1

printdown('报名人数')

#### 成绩查询信息储存 ####
tablename = '成绩查询表'
sql = f"CREATE TABLE {tablename} (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), html VARCHAR(255))"
mysql.create_table(sql)

id = 1

for i in range(len(grade)):
    value = (id, grade[i], grade_link_x[i])
    sql = f"insert into {tablename} values {value}"
    mysql.commit_data(sql)
    id += 1


#### 分数线储存 ####
# 当年分数线
gradeline_essay_total = ''
for i in gradeline_essay:
    gradeline_essay_total += i
title = f'{gradeline[0]}.txt'
with open(title, 'w') as f:
    f.write(gradeline_essay_total)
# 历年分数线
for i in range(5):
    title = f'{gradeline_table[2+2*i]}年{gradeline_table[1]}.txt'
    with open(title, 'w') as f:
        f.write(gradeline_table[3+2*i])

printdown('分数线')

##### 面试名单信息储存 #####
tablename = '面试名单表'
sql = f"CREATE TABLE {tablename} (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), html VARCHAR(255))"
mysql.create_table(sql)

id = 1

for i in range(len(interview)):
    value = (id, interview[i], interview_link_x[i])
    sql = f"insert into {tablename} values {value}"
    mysql.commit_data(sql)
    id += 1

printdown(tablename)

##### 调剂职位信息储存 #####
tablename = '调剂职位表'
sql = f"CREATE TABLE {tablename} (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), html VARCHAR(255))"
mysql.create_table(sql)

id = 1

for i in range(len(adjust)):
    value = (id, adjust[i], adjust_link_x[i])
    sql = f"insert into {tablename} values {value}"
    mysql.commit_data(sql)
    id += 1

printdown(tablename)

##### 录用公示 #####
tablename = '录用公示表'
sql = f"CREATE TABLE {tablename} (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), html VARCHAR(255))"
mysql.create_table(sql)

id = 1

for i in range(len(employ)):
    value = (id, employ[i], employ_link_x[i])
    sql = f"insert into {tablename} values {value}"
    mysql.commit_data(sql)
    id += 1

printdown(tablename)

##### 补录公告 #####
tablename = '补录公告表'
sql = f"CREATE TABLE {tablename} (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), html VARCHAR(255))"
mysql.create_table(sql)

id = 1

for i in range(len(hot_collection)):
    value = (id, hot_collection[i], hot_collection_link_x[i])
    sql = f"insert into {tablename} values {value}"
    mysql.commit_data(sql)
    id += 1

printdown(tablename)

##### 考试政策 #####
tablename = '考试政策表'
sql = f"CREATE TABLE {tablename} (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), html VARCHAR(255))"
mysql.create_table(sql)

id = 1

for i in range(len(policy)):
    value = (id, policy[i], policy_link_x[i])
    sql = f"insert into {tablename} values {value}"
    mysql.commit_data(sql)
    id += 1

printdown(tablename)
