# coding=utf-8

import logging
import json
import constants
import math
from  urllib import unquote

from handlers.BaseHandler import BaseHandler
from utils.response_code import RET
from utils.commons import required_login
from utils.commons import ComplexEncoder

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class HouseInfoHandler(BaseHandler):
    """房屋信息"""

    def post(self):
        pass

    def get(self, community):
        """获取房屋信息"""

        stime = self.get_argument("stime")
        community_name = unquote(community)
        print(type(community_name))



        # 查询数据库

        # 查询房屋基本信息
        #sql = "select a.totalPrice,a.unitPrice,a.years,a.title,a.square,a.link,a.housetype, a.floor,a.status,a.houseID,a.direction,a.community,a.totalPrice,taxtype from sellinfo a,houseinfo b where a.community=b.community and a.community=%s" % community_name
        sql = "select * from houseinfo  where community like '%%%s%%'" % (community_name)

        try:
            print('sql=%s' % sql)
            ret = self.db.query(sql)
        #print("查到的数据：%s" % ret)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="查询错误"))


        # 用户查询的可能是不存在的房屋id, 此时ret为None
        if not ret:
            return self.write(dict(errcode=RET.NODATA, errmsg="查无此房"))

        sell_house_list = []
        for item in ret:
            data = {
                "HouseID":item["houseID"],
                "Direction":item["direction"],
                "Decoration": item["decoration"],
                "Floor":item["floor"],
                "Housetype":item["housetype"],
                "Link":item["link"],
                "Square":item["square"],
                "Title":item["title"],
                "TotalPrice":item["totalPrice"],
                "UnitPrice":item["unitPrice"],
                "Years":item["years"],
                "Taxtype": item["taxtype"]

            }
            sell_house_list.append(data)

        data_json = json.dumps(sell_house_list)


        resp = '{"data":%s}' % (data_json)
        self.write(resp)



class HouseTypeHandler(BaseHandler):
    """房屋信息"""

    def post(self):
        pass

    def get(self, community):
        """获取房屋信息"""

        stime = self.get_argument("stime")
        community_name = unquote(community)
        #print(community_name)



        # 查询数据库

        # 查询房屋基本信息
        #sql = "select a.housetype as Zone, count(*) as Num,avg(a.unitprice) as Price from sellinfo a,houseinfo b where a.community=b.community and a.community like '%%%s%%' group by a.housetype;" % community_name
        sql = "select housetype as Zone, count(*) as Num,avg(unitprice) as Price from sellinfo  where  community like '%%%s%%' group by housetype;" % community_name

        try:
            ret = self.db.query(sql )
            #print("查到的数据：%s" % ret)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="查询错误"))

        # 用户查询的可能是不存在的房屋id, 此时ret为None
        if not ret:
            return self.write(dict(errcode=RET.NODATA, errmsg="查无此房"))

        house_type_list = []
        for item in ret:
            data = {
                "Zone":item["Zone"],
                "Price":item["Price"],

            }
            house_type_list.append(data)

        data_json = json.dumps(house_type_list)


        resp = '{"data":%s}' % (data_json)
        self.write(resp)


class RentZoneHandler(BaseHandler):
    """房屋信息"""

    def post(self):
        pass

    def get(self, community):
        """获取房屋信息"""

        stime = self.get_argument("stime")
        etime = self.get_argument("etime")
        community_name = unquote(community)
        #print(community_name)



        # 查询数据库

        # 查询房屋基本信息
        sql = "select zone as Zone, count(*) as Num,avg(price) as Price from rentinfo  where region like '%%%s%%' group by zone;" % community_name


        try:
            ret = self.db.query(sql)
            #print("查到的数据：%s" % ret)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="查询错误"))

        # 用户查询的可能是不存在的房屋id, 此时ret为None
        if not ret:
            return self.write(dict(errcode=RET.NODATA, errmsg="查无此房"))

        rent_type_list = []
        for item in ret:
            data = {
                "Zone":item["Zone"],
                "Price":item["Price"],

            }
            rent_type_list.append(data)

        data_json = json.dumps(rent_type_list)


        resp = '{"data":%s}' % (data_json)
        self.write(resp)



class RentInfoHandler(BaseHandler):
    """房屋信息"""

    def post(self):
        pass

    def get(self, community):
        """获取房屋信息"""

        stime = self.get_argument("stime")
        etime = self.get_argument("etime")
        community_name = unquote(community)
        #print(community_name)



        # 查询数据库

        # 查询房屋基本信息
        sql = "select * from rentinfo where region like '%%%s%%'" % community_name


        try:
            ret = self.db.query(sql)
            #print("查到的数据：%s" % ret)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="查询错误"))

        # 用户查询的可能是不存在的房屋id, 此时ret为None
        if not ret:
            return self.write(dict(errcode=RET.NODATA, errmsg="查无此房"))

        rent_info_list = []
        for item in ret:
            data = {
                "Zone":item["zone"],
                "Price":item["price"],
                "Meters": item["meters"],
                "Decoration": item["decoration"],
                "Heating": item["heating"],
                "Other": item["other"],

            }
            rent_info_list.append(data)

        data_json = json.dumps(rent_info_list)


        resp = '{"data":%s}' % (data_json)
        self.write(resp)


class SellInfoHandler(BaseHandler):
    """房屋信息"""

    def post(self):
        pass

    def get(self, community):
        """获取房屋信息"""

        stime = self.get_argument("stime")
        etime = self.get_argument("etime")
        sort = self.get_argument("sort")
        order = self.get_argument("order")
        community_name = unquote(community)
        #print(community_name)
        #print('sort',sort)
        #print('order',order)
        if sort == u'TotalPrice':
            sort = u'totalPrice'
            sql = "select * from sellinfo where community like '%%%s%%' order by cast(%s as int) %s;" % (community_name, sort, order)
        elif  sort == u'Dealdate':
            sort = u'dealdate'
            sql = "select * from sellinfo where community like '%%%s%%' order by %s %s;" % (community_name, sort, order)
        elif  sort == u'Status':
            sort = u'status'
            sql = "select * from sellinfo where community like '%%%s%%' order by %s %s;" % (community_name, sort, order)
        else:
            sort = u'housetype'
            sql = "select * from sellinfo where community like '%%%s%%' order by %s %s;" % (community_name, sort, order)

        #print('sort', sort)

        # 查询数据库

        # 查询房屋基本信息


        #print("sql=%s" % sql)
        try:
            ret = self.db.query(sql)
            #print("查到的数据：%s" % ret)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="查询错误"))

        # 用户查询的可能是不存在的房屋id, 此时ret为None
        if not ret:
            return self.write(dict(errcode=RET.NODATA, errmsg="查无此房"))

        sell_info_list = []
        for item in ret:
            data = {
                "Square":item["square"],
                "TotalPrice":item["totalPrice"],
                "UnitPrice": item["unitPrice"],
                "Dealdate": item["dealdate"],
                "Years": item["years"],
                "Housetype": item["housetype"],
                "Direction": item["direction"],
                "Floor": item["floor"],
                "Status": item["status"],
                "Source": item["source"],
                "Title": item["title"]

            }
            sell_info_list.append(data)

        #print('sell_info_list=%s' % sell_info_list)
        data_json = json.dumps(sell_info_list)


        resp = '{"data":%s}' % (data_json)
        self.write(resp)



class communityTitleHandler(BaseHandler):
    """房屋信息"""

    def post(self):
        pass

    def get(self, community):
        """获取房屋信息"""

        community_name = unquote(community)
        #print(community_name)


        # 查询数据库

        # 查询房屋基本信息
        sql = "select * from community where title like '%%%s%%'" % community_name

        #print("sql=%s" % sql)
        try:
            ret = self.db.query(sql)
            #print("查到的数据：%s" % ret)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="查询错误"))

        # 用户查询的可能是不存在的房屋id, 此时ret为None
        if not ret:
            return self.write(dict(errcode=RET.NODATA, errmsg="查无此房"))

        community_title_list = []
        for item in ret:
            data = {
                "District":item["district"],
                "Year":item["year"],
                "Housetype": item["housetype"],
                "Cost": item["cost"],
                "Service": item["service"],
                "Company": item["company"],
                "BuildingNum": item["building_num"],
                "Title": item["title"],
                "HouseNum": item["house_num"]

            }
            community_title_list.append(data)

        #print('community_title_list=%s' % community_title_list)
        data_json = json.dumps(community_title_list)


        resp = '{"data":%s}' % (data_json)
        self.write(resp)


class SellCountHandler(BaseHandler):
    """房屋信息"""

    def post(self):
        pass

    def get(self, type, community):
        """获取房屋信息"""

        stime = self.get_argument("stime")
        etime = self.get_argument("etime")
        community_name = unquote(community)
        #print(community_name)
        #print(type)

        # 查询数据库

        # 查询房屋基本信息
        sql = "select %s as type,count(*) as total from sellinfo where community like '%%%s%%' group by %s" % (type, community_name, type)

       # print("sql=%s" % sql)
        try:
            ret = self.db.query(sql)
            #print("查到的数据：%s" % ret)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="查询错误"))

        # 用户查询的可能是不存在的房屋id, 此时ret为None
        if not ret:
            return self.write(dict(errcode=RET.NODATA, errmsg="查无此房"))

        sell_count_list = []
        for item in ret:
            data = {
                "Total":item["total"],
                "Type":item["type"]

            }
            sell_count_list.append(data)

        #print('sell_count_list=%s' % sell_count_list)
        data_json = json.dumps(sell_count_list)
        resp = '{"data":%s}' % (data_json)
        self.write(resp)



class CommunityBizcircleInfoHandler(BaseHandler):
    """房屋信息"""

    def post(self):
        pass

    def get(self, bizcircle):
        """获取房屋信息"""

        bizcircle_name = unquote(bizcircle)
        #print(bizcircle_name)


        # 查询数据库

        # 查询房屋基本信息
        sql = "select * from community where bizcircle like '%%%s%%' " % bizcircle_name
        #print("sql=%s" % sql)
        try:
            ret = self.db.query(sql)
            #print("查到的数据：%s" % ret)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="查询错误"))

        # 用户查询的可能是不存在的房屋id, 此时ret为None
        if not ret:
            return self.write(dict(errcode=RET.NODATA, errmsg="查无此房"))

        bizcircle_list = []
        for item in ret:
            data = {
                "District":item["district"],
                "Price":item["price"],
                "Onsale": item["onsale"],
                "Onrent": item["onrent"],
                "Year": item["year"],
                "Cost": item["cost"],
                "Service": item["service"],
                "Company": item["company"],
                "BuildingNum": item["building_num"],
                "HouseNum": item["house_num"],
                "Title": item["title"],
                "Housetype": item["housetype"]

            }
            bizcircle_list.append(data)

        #print('bizcircle_list=%s' % bizcircle_list)
        data_json = json.dumps(bizcircle_list)
        resp = '{"data":%s}' % (data_json)
        self.write(resp)



class BizcircleInfoHandler(BaseHandler):
    """房屋信息"""

    def post(self):
        pass

    def get(self):
        """获取房屋信息"""
        district_name = unquote(self.get_argument('district'))

        #print(district_name)


        # 查询数据库

        # 查询房屋基本信息
        sql = "select distinct district,bizcircle from community where district like '%%%s%%'" % district_name
        #print("sql=%s" % sql)
        try:
            ret = self.db.query(sql)
            #print("查到的数据：%s" % ret)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="查询错误"))

        # 用户查询的可能是不存在的房屋id, 此时ret为None
        if not ret:
            return self.write(dict(errcode=RET.NODATA, errmsg="查无此房"))

        bizcircle_list = []
        for item in ret:
            data = {
                "District":item["district"],
                "Bizcircle": item["bizcircle"]

            }
            bizcircle_list.append(data)

        #print('bizcircle_list=%s' % bizcircle_list)
        data_json = json.dumps(bizcircle_list)
        resp = '{"data":%s}' % (data_json)
        self.write(resp)

class BizcircleCommunityHandler(BaseHandler):
    """房屋信息"""

    def post(self):
        pass

    def get(self):
        """获取房屋信息"""
        bizcircle_name = unquote(self.get_argument('bizcircle'))

        #print(bizcircle_name)


        # 查询数据库

        # 查询房屋基本信息
        sql = "select distinct district,bizcircle from community where district like '%%%s%%'" % bizcircle_name
        #print("sql=%s" % sql)
        try:
            ret = self.db.query(sql)
            #print("查到的数据：%s" % ret)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="查询错误"))

        # 用户查询的可能是不存在的房屋id, 此时ret为None
        if not ret:
            return self.write(dict(errcode=RET.NODATA, errmsg="查无此房"))

        bizcircle_list = []
        for item in ret:
            data = {
                "District":item["district"],
                "Bizcircle": item["bizcircle"]

            }
            bizcircle_list.append(data)

        #print('bizcircle_list=%s' % bizcircle_list)
        data_json = json.dumps(bizcircle_list)
        resp = '{"data":%s}' % (data_json)
        self.write(resp)