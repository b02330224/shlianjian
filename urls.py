# coding:utf-8

import os

#from handlers.BaseHandler import StaticFileBaseHandler as StaticFileHandler
from handlers import  House
from tornado.web import StaticFileHandler

current_path = os.path.dirname(__file__)
urls = [
    # (r"/log", Passport.LogHandler),
    (r"/api/house/info/(.*)", House.HouseInfoHandler),
    (r"/api/house/type/(.*)", House.HouseTypeHandler),
    (r"/api/rent/info/(.*)", House.RentInfoHandler),
    (r"/api/rent/zone/(.*)", House.RentZoneHandler),
    (r"/api/sell/info/(.*)", House.SellInfoHandler),
    (r"/api/sell/(.*)/count/(.*)", House.SellCountHandler),
    (r"/api/community/title/(.*)", House.communityTitleHandler),
    (r"/api/community/bizcircle/info/(.*)", House.CommunityBizcircleInfoHandler),
    (r"/api/bizcircle", House.BizcircleInfoHandler),
    #(r"/community.html", House.BizcircleCommunityHandler),
    (r"^/(.*)", StaticFileHandler,  {"path": os.path.join(current_path, "html"), "default_filename": "houseinfo.html"}),

    #(r"/(.*)", StaticFileHandler,  dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html"))
]

