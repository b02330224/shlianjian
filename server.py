# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import os
import torndb
import config


from urls import urls
from tornado.options import options, define
from tornado.web import RequestHandler
from utils.sqlitedb import SqliteDb

define("port", default=8001, type=int, help="run server on the given port")


class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        #self.db = torndb.Connection(**config.mysql_options)
        self.db = SqliteDb(config.sqlite3_db_file)




def main():
    options.log_file_prefix = config.log_path
    options.logging = config.log_level
    tornado.options.parse_command_line()
    app = Application(
        urls,
        **config.settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()