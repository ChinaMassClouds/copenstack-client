#/usr/bin/python
#coding:utf-8

import pymongo
import sys
from datetime import  timedelta
import datetime

class Remove(object):

     def __init__(self,host_ip,port=27017):
       """
       :param host_ip : 数据库绑定IP
       :param port : 数据库绑定端口 默认27017
       """
       try:
          self._conn = pymongo.Connection(host_ip,port)
       except Exception,e:
          print e


     def removeOldData(self,db_name,collection_name,timestamp_name):
         """
         :param db_name : 数据库名称
         :param collection_name : 集合名称
         :param timestamp_name : 时间戳字段名称
         """
         remove_date = datetime.datetime.today() - timedelta(days = 2)
         print "remove_date", remove_date, type(remove_date) 
         op = self._conn[db_name][collection_name]
         op.remove({timestamp_name:{"$lt":remove_date}})
     
     def remove(self):
         self.removeOldData("ceilometer","meter","timestamp")
      
     def removeAlarmHistory(self):
         self.removeOldData("ceilometer","alarm_history","timestamp")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "ths number of argv is few"
        sys.exit(1)

    HOST_IP = sys.argv[1]
    r = Remove(HOST_IP)
    r.remove()
    r.removeAlarmHistory()
