# -*- coding: utf-8 -*-
# boss直聘爬虫
   
import requests
from bs4 import BeautifulSoup
import time
import re
from openpyxl import Workbook
import uuid
import cx_Oracle as cxo


url_base = "www.zhipin.com"
headers = {
    'x-devtools-emulate-network-conditions-client-id': "5f2fc4da-c727-43c0-aad4-37fce8e3ff39",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'dnt': "1",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.8,en;q=0.6",
    'cookie': "__c=1501326829; lastCity=101020100; __g=-; __l=r=https%3A%2F%2Fwww.google.com.hk%2F&l=%2F; __a=38940428.1501326829..1501326829.20.1.20.20; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1501326839; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1502948718; __c=1501326829; lastCity=101020100; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1501326839; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1502954829; __l=r=https%3A%2F%2Fwww.google.com.hk%2F&l=%2F; __a=38940428.1501326829..1501326829.21.1.21.21",
    'cache-control': "no-cache",
    'postman-token': "76554687-c4df-0c17-7cc0-5bf3845c9831"
}

# 爬取页面
def get_list(keywords, page_num):
	list_url = "https://www.zhipin.com/c101010100/h_101010100/?query=" + keywords + "&page=" + page_num
	html = requests.get(list_url, headers=headers)

	if html.status_code == 200:  # 爬的太快网站返回403，只能等着
		soup = BeautifulSoup(html.text, "html.parser")
		# job_list = soup.select(".job-title")
		job_detail_list = soup.select(".job-primary .info-primary .name")
		time.sleep(20)  # 注意休息，否则会死

		return job_detail_list


# 解析页面
def deal_with_data(keywords, page_num, job_detail_list):
	lst = []
	for i in job_detail_list:
		dic = {}
		job_detail_url = url_base + re.findall(".*href=\"(.*)\" ka=.*",str(i))[0]
		# print(job_detail_url)
		jobid = re.findall(".*data-jobid=\"(.*)\" data-lid=.*",str(i))[0]
		# print(jobid)
		dic['uuid'] = uuid.uuid1()
		dic['page_num'] = page_num
		dic['keywords'] = keywords
		dic['jobid'] = jobid
		dic['job_detail_url'] = job_detail_url
		lst.append(dic)

	return lst

# 获取数据库连接
def getConfig():
    oracleHost = "127.0.0.1"
    oraclePort = "1521"
    oracleUser = "scott"
    oraclePassword = "tiger"
    oracleDatabaseName = "orcl"
    oracleConn = oracleUser + '/' + oraclePassword + '@' + oracleHost + '/' + oracleDatabaseName
    conn = cxo.connect(oracleConn)
    cursor = conn.cursor()
    print("已获取数据库连接")
    return cursor

# 插入数据库
def save_in_db(lst):
	for i in lst:
		print(i)
		sql_str = "insert when (not exists (select job_detail_url from boss_job_list \
			where job_detail_url = :job_detail_url)) \
			then into boss_job_list(uuid, page_num, keywords, jobid, \
			job_detail_url) values(:uuid, :page_num, :keywords, :jobid, :job_detail_url) \
			select :job_detail_url from dual"
		cursor.execute(sql_str, (
				str(i['job_detail_url']), str(i['uuid']), str(i['page_num']), str(i['keywords']), 
				str(i['jobid']), str(i['job_detail_url']), str(i['job_detail_url'])
			) )
	cursor.execute("commit")


if __name__ == '__main__':
	cursor = getConfig()
	print(cursor)

	keywords = '风控'
	for i in range(1, 100):
		page_num = str(i)
		job_detail_list = get_list(keywords, page_num)
		lst = deal_with_data(keywords, page_num, job_detail_list)
		save_in_db(lst)
		print(keywords, '第', i, '页，存储完毕')
		# print(lst)
	
	
		
