# coding:utf-8
import sqlite3
import os
import itertools


class Row(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


class SqliteDb(object):
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        print(self.db_name )
        self.connect()

    def connect(self):
        if os.path.exists(self.db_name) and os.path.isfile(self.db_name):
            conn = sqlite3.connect(self.db_name)
            self.conn = conn
            print('conn=%s' % self.conn)
        else:
            print("文件不存在")

    def close(self):
        self.conn.close()

    def get(self, sql):

        rows = self.query(sql)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for Database.get() query")
        else:
            return rows[0]


    def query(self, sql):
        print("sql=%s" % sql)
        print('dir(conn)=%s' % dir(self.conn))
        cursor = self.conn.cursor()
        print("Opened database successfully")

        #try:
        cursor = cursor.execute(sql)
        rs = cursor.fetchall()
        print(type(rs))
        print("cursor=%s" % cursor)
        print("dir(cursor)=%s" % dir(cursor))
        print( cursor.description)

        column_names = [d[0] for d in cursor.description]
        return [Row(itertools.izip(column_names, row)) for row in rs]
        #print("rs=%s" % rs)

        print("Operation done successfully")
        #finally:
        cursor.close()