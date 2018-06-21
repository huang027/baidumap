import requests
import re
import csv
import time
import json
import pandas as pd
import os

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36(KHTML, like Gecko) Chrome/56.0.2924.87Safari/537.36'}


class Mapdata(object):
	"""
	使用方法：
	
	fetch_hot_citys(self,keyword) 获取该关键词的热门城市
	get_city_codes(self,keyword,csvpath) 获取该关键词店铺全国城市码
	fetch_one_city_data(self, citycode, keyword) 获取指定城市码指定关键词的行业数据
	fetch_all_city_data(self, keyword) 获取全国城市指定关键词的行业数据
	"""
	
	def __init__(self,filepath,sleeptime=1000):
		"""
		
		:param filepath: csv文件的路径，用来存数据
		:param sleeptime: 访问频率。默认为1s
		"""
		self.csvf = open(filepath,'a+',encoding='gbk',newline='')
		self.writer = csv.writer(self.csvf)
		self.writer.writerow(("name", "province_name", "city_name", "city_code","area", "addr", "geo", "poi_address","catalogID", "std_tag", "img_url", "price", "overall_rating", "telephone","mobilephone"))
		self.sleeptime = sleeptime/1000

		
	def requests_module(self,citycode,keyword,pageno):
		"""
		请求模板，其他方法都是以此为基础
		:param citycode: 城市码
		:param keyword: 关键词
		:param pageno: 页码数
		:return:
		"""
		parameter = {
			"newmap": "1",
			"reqflag": "pcmap",
			"biz": "1",
			"from": "webmap",
			"da_par": "direct",
			"pcevaname": "pc4.1",
			"qt": "con",
			"c": citycode,  # 城市代码
			"wd": keyword,  # 搜索关键词
			"wd2": "",
			"pn": pageno,  # 页数
			"nn": pageno * 10,
			"db": "0",
			"sug": "0",
			"addr": "0",
			"da_src": "pcmappg.poi.page",
			"on_gel": "1",
			"src": "7",
			"gr": "3",
			"l": "12",
			"tn": "B_NORMAL_MAP",  # "u_loc": "12621219.536556,2630747.285024",
			"ie": "utf-8",  # "b": "(11845157.18,3047692.2;11922085.18,3073932.2)",  #这个应该是地理位置坐标，可以忽略
			"t": str(time.time()).replace('.', '')[:13]}
		
		url = 'http://map.baidu.com/'
		html = requests.get(url, params=parameter, headers=headers)
		transform_html = html.text.encode('latin-1').decode('unicode_escape')
		jsondatas = json.loads(transform_html)
		return jsondatas
	
	def fetch_one_city_data(self, citycode, keyword):
		"""
		获取一个城市码（citycode）的关键词keyword行业的信息
		:return:
		"""
		Flag = True
		pageno = 1
		while Flag:
			jsondatas = self.requests_module(citycode,keyword,pageno)
			if jsondatas.get("content"):
				self.parse_data(jsondatas)
			else:
				Flag = False
				
			time.sleep(self.sleeptime)
			pageno+=1
		self.csvf.close()
		
	
	def fetch_all_city_data(self,keyword):
		"""
		获取全国keyword行业的信息
		:return:
		"""
		for citycode in range(35,400):
			try:
				Flag = True
				pageno = 1
				while Flag:
					jsondatas = self.requests_module(citycode, keyword, pageno)
					if jsondatas.get("content"):
						self.parse_data(jsondatas)
					else:
						Flag = False
						
					time.sleep(self.sleeptime)
					pageno+=1
			except:
				print('这个城市不存在对应城市',citycode,'继续下一个城市码')
			
	
	def parse_data(self,jsondatas):
		"""
		对请求到的含有商业信息的json数据进行解析，抽取有价值的信息。如商户名、地址、联系方式、类目、评分、价格等
		:param jsondatas:  含有商业信息的json数据
		:return:
		"""
		province_name = jsondatas['current_city']['up_province_name']
		city_name = jsondatas['current_city']['name']
		city_code = jsondatas['current_city']['code']
		
		for jsd in jsondatas.get("content"):
			
			area = jsd['area_name']
			addr = jsd['addr']
			catalogID = jsd['catalogID']
			name = jsd['name']
			std_tag = jsd['std_tag']
			geo = jsd['geo']
			try:
				detail_info = jsd['ext']['detail_info']
				img_url = detail_info['image']
				overall_rating = detail_info['overall_rating']
				phone = detail_info['phone']
				poi_address = detail_info['poi_address']
				price = detail_info['price']
				print(name, area, addr, std_tag, phone)
				only_mobilephones = re.findall(r'1\d{10}', phone)
				for mobilephone in only_mobilephones:
					self.writer.writerow((name, province_name, city_name, city_code, area, addr, geo,poi_address, catalogID, std_tag, img_url, price, overall_rating,phone,mobilephone))
			
			
			except:
				continue
				
	def fetch_hot_citys(self,keyword):
		"""
		只需要输入keyword获取该词的热门城市列表[(city1,code1),(city2,code2)...]
		:param keyword: 行业关键词
		:return: 返回城市列表
		"""
		
		pageno,city = 1,131  #随便写的，这里不用纠结
		jsondatas = self.requests_module(city, keyword, pageno)
		hot_citys = jsondatas['hot_city']
		hot_citys = [tuple(c.split('|')) for c in hot_citys]
		return hot_citys


	

	
	
		
