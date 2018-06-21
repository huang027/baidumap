from baidumap.baidumap import Mapdata
import os
'''
fetch_hot_citys(self,keyword) #获取该关键词的热门城市
fetch_one_city_data(self, citycode, keyword) #获取指定城市码指定关键词的行业数据
fetch_all_city_data(self, keyword) #获取全国城市指定关键词的行业数据
'''
#初始化,建立一个csv文件用于存储数据
keyword = '丝网'
citycode = 131   #北京市的城市码
filepath = 'data.csv'
sleeptime = 100   #调节访问速度，默认为1000（即1s）

md = Mapdata(filepath=filepath,sleeptime=sleeptime)

#获取百度地图上该关键词的热门城市列表
hot_citys = md.fetch_hot_citys(keyword=keyword)
print(hot_citys)


#获取指定城市指定关键词的行业数据
md.fetch_one_city_data(citycode=citycode, keyword=keyword)


#获取全国该关键词的商家信息
md.fetch_all_city_data(keyword=keyword)