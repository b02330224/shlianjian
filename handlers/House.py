# coding:utf-8

import logging
import json
import constants
import math
from  urllib import unquote

from handlers.BaseHandler import BaseHandler
from utils.response_code import RET
from utils.commons import required_login
from utils.commons import ComplexEncoder


class HouseInfoHandler(BaseHandler):
    """房屋信息"""
    @required_login
    def post(self):
        """保存"""
        # 获取参数
        """{
            "title":"",
            "price":"",
            "area_id":"1",
            "address":"",
            "room_count":"",
            "acreage":"",
            "unit":"",
            "capacity":"",
            "beds":"",
            "deposit":"",
            "min_days":"",
            "max_days":"",
            "facility":["7","8"]
        }"""

        user_id = self.session.data.get("user_id")
        title = self.json_args.get("title")
        price = self.json_args.get("price")
        area_id = self.json_args.get("area_id")
        address = self.json_args.get("address")
        room_count = self.json_args.get("room_count")
        acreage = self.json_args.get("acreage")
        unit = self.json_args.get("unit")
        capacity = self.json_args.get("capacity")
        beds = self.json_args.get("beds")
        deposit = self.json_args.get("deposit")
        min_days = self.json_args.get("min_days")
        max_days = self.json_args.get("max_days")
        facility = self.json_args.get("facility") # 对一个房屋的设施，是列表类型
        # 校验
        if not all((title, price, area_id, address, room_count, acreage, unit, capacity, beds, deposit, min_days,
                    max_days)):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="缺少参数"))

        try:
            price = int(price) * 100
            deposit = int(deposit) * 100
        except Exception as e:
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数错误"))

        # 数据
        try:
            sql = "insert into ih_house_info(hi_user_id,hi_title,hi_price,hi_area_id,hi_address,hi_room_count," \
                  "hi_acreage,hi_house_unit,hi_capacity,hi_beds,hi_deposit,hi_min_days,hi_max_days) " \
                  "values(%(user_id)s,%(title)s,%(price)s,%(area_id)s,%(address)s,%(room_count)s,%(acreage)s," \
                  "%(house_unit)s,%(capacity)s,%(beds)s,%(deposit)s,%(min_days)s,%(max_days)s)"
            # 对于insert语句，execute方法会返回最后一个自增id
            house_id = self.db.execute(sql, user_id=user_id, title=title, price=price, area_id=area_id, address=address,
                                       room_count=room_count, acreage=acreage, house_unit=unit, capacity=capacity,
                                       beds=beds, deposit=deposit, min_days=min_days, max_days=max_days)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg="save data error"))


        # house_id = 10001
        # facility = ["7", "8", "9", "10"]
        #
        # """
        # hf_id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
        # hf_house_id bigint unsigned NOT NULL COMMENT '房屋id',
        # hf_facility_id int unsigned NOT NULL COMMENT '房屋设施',
        # hf_ctime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
        # """
        # hf_id    hf_house_id    hf_facility_id
        # 1       10001           7
        # 2       10001           8
        # 3       10001           9
        #
        # sql_val = []
        # for facility_id in facility:
        #     sql = "insert into ih_house_facility(hf_house_id, hf_facility_id) " \
        #           "value(%s, %s),(%s, %s),(%s, %s)"
        #     sql_val.append(facility_id)
        #
        # sql_val = tuple(sql_val)
        #     try:
        #         self.db.execute(sql, *sql_val)





        try:
            # for fid in facility:
            #     sql = "insert into ih_house_facility(hf_house_id,hf_facility_id) values(%s,%s)"
            #     self.db.execute(sql, house_id, fid)
            sql = "insert into ih_house_facility(hf_house_id,hf_facility_id) values"
            sql_val = [] # 用来保存条目的(%s, %s)部分  最终的形式 ["(%s, %s)", "(%s, %s)"]
            vals = []  # 用来保存的具体的绑定变量值
            for facility_id in facility:
                # sql += "(%s, %s)," 采用此种方式，sql语句末尾会多出一个逗号
                sql_val.append("(%s, %s)")
                vals.append(house_id)
                vals.append(facility_id)

            sql += ",".join(sql_val)
            vals = tuple(vals)
            logging.debug(sql)
            logging.debug(vals)
            self.db.execute(sql, *vals)
        except Exception as e:
            logging.error(e)
            try:
                self.db.execute("delete from ih_house_info where hi_house_id=%s", house_id)
            except Exception as e:
                logging.error(e)
                return self.write(dict(errcode=RET.DBERR, errmsg="delete fail"))
            else:
                return self.write(dict(errcode=RET.DBERR, errmsg="no data save"))
        # 返回
        self.write(dict(errcode=RET.OK, errmsg="OK", house_id=house_id))

    def get(self, community):
        """获取房屋信息"""

        stime = self.get_argument("stime")
        community_name = unquote(community)
        print(community_name)



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
        # self.write(dict(errcode=RET.OK, errmsg="OK", data=data))
        self.write(resp)



class HouseTypeHandler(BaseHandler):
    """房屋信息"""

    def post(self):
        pass

    def get(self, community):
        """获取房屋信息"""

        stime = self.get_argument("stime")
        community_name = unquote(community)
        print(community_name)



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
        # self.write(dict(errcode=RET.OK, errmsg="OK", data=data))
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
        print(community_name)



        # 查询数据库

        # 查询房屋基本信息
        sql = "select zone as Zone, count(*) as Num,avg(price) as Price from rentinfo  where region like '%%%s%%' group by zone;" % community_name


        try:
            ret = self.db.query(sql)
            print("查到的数据：%s" % ret)
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
        # self.write(dict(errcode=RET.OK, errmsg="OK", data=data))
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
        print(community_name)



        # 查询数据库

        # 查询房屋基本信息
        sql = "select * from rentinfo where region like '%%%s%%'" % community_name


        try:
            ret = self.db.query(sql)
            print("查到的数据：%s" % ret)
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
        # self.write(dict(errcode=RET.OK, errmsg="OK", data=data))
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
        print(community_name)
        print('sort',sort)
        print('order',order)
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

        print('sort', sort)

        # 查询数据库

        # 查询房屋基本信息


        print("sql=%s" % sql)
        try:
            ret = self.db.query(sql)
            print("查到的数据：%s" % ret)
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

        print('sell_info_list=%s' % sell_info_list)
        data_json = json.dumps(sell_info_list)


        resp = '{"data":%s}' % (data_json)
        # self.write(dict(errcode=RET.OK, errmsg="OK", data=data))
        self.write(resp)



class communityTitleHandler(BaseHandler):
    """房屋信息"""

    def post(self):
        pass

    def get(self, community):
        """获取房屋信息"""

        community_name = unquote(community)
        print(community_name)


        # 查询数据库

        # 查询房屋基本信息
        sql = "select * from community where title like '%%%s%%'" % community_name

        print("sql=%s" % sql)
        try:
            ret = self.db.query(sql)
            print("查到的数据：%s" % ret)
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

        print('community_title_list=%s' % community_title_list)
        data_json = json.dumps(community_title_list)


        resp = '{"data":%s}' % (data_json)
        # self.write(dict(errcode=RET.OK, errmsg="OK", data=data))
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
        print(community_name)
        print(type)

        # 查询数据库

        # 查询房屋基本信息
        sql = "select %s as type,count(*) as total from sellinfo where community like '%%%s%%' group by %s" % (type, community_name, type)

        print("sql=%s" % sql)
        try:
            ret = self.db.query(sql)
            print("查到的数据：%s" % ret)
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

        print('sell_count_list=%s' % sell_count_list)
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
        print(bizcircle_name)


        # 查询数据库

        # 查询房屋基本信息
        sql = "select * from community where bizcircle like '%%%s%%' " % bizcircle_name
        print("sql=%s" % sql)
        try:
            ret = self.db.query(sql)
            print("查到的数据：%s" % ret)
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

        print('bizcircle_list=%s' % bizcircle_list)
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

        print(district_name)


        # 查询数据库

        # 查询房屋基本信息
        sql = "select distinct district,bizcircle from community where district like '%%%s%%'" % district_name
        print("sql=%s" % sql)
        try:
            ret = self.db.query(sql)
            print("查到的数据：%s" % ret)
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

        print('bizcircle_list=%s' % bizcircle_list)
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

        print(bizcircle_name)


        # 查询数据库

        # 查询房屋基本信息
        sql = "select distinct district,bizcircle from community where district like '%%%s%%'" % bizcircle_name
        print("sql=%s" % sql)
        try:
            ret = self.db.query(sql)
            print("查到的数据：%s" % ret)
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

        print('bizcircle_list=%s' % bizcircle_list)
        data_json = json.dumps(bizcircle_list)
        resp = '{"data":%s}' % (data_json)
        self.write(resp)