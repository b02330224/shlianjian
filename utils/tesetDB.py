# coding:utf-8
from sqlitedb import SqliteDb

sqlite = SqliteDb('/opt/lianjia_scrawler/lianjia-scrawler/lianjiash.db')
sql = "select * from community  where bizcircle='静安寺'"
c_lst = sqlite.query(sql)
print(c_lst[0])
sqlite.close()