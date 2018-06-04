# shlianjian
这是一个查询上海小区售房租房的web网站，使用tornado + bootstrap开发

## 介绍
这是一个查询上海小区售房租房的web网站，后台使用tornado+sqlite3，前端使用jQuery,bootstrap sb-admin template开发.
数据是自己写的爬虫，从链家网站上爬取下来的,目前只支持静安，长宁，杨浦，浦东四个区的房源信息。

## 在线演示地址：https://shlianjia.herokuapp.com

![](https://github.com/b02330224/shlianjian/blob/master/zsfy.png)
![](https://github.com/b02330224/shlianjian/blob/master/sqfx.png)


## 使用说明
1. git clone git@github.com:b02330224/shlianjian.git
2. cd shlianjian
#### If you'd like not to use [virtualenv](https://virtualenv.pypa.io/en/stable/), please skip step 3 and 4.
3. virtualenv lianjia
4. source lianjia/bin/activate
5. pip install -r requirements.txt
6. python server.py
