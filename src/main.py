# This is a sample Python script.
import datetime
import sys
import time
import threading
import inspect
import ctypes
import requests
import json
import urllib3
import jsonpath
import os


from PyQt5 import QtWidgets, uic
from PyQt5.Qt import *

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDesktopWidget#桌面类
from PyQt5.QtWidgets import QApplication



from MainWindow import Ui_MainWindow
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


NEWPOST = True

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# class MyTimer(hours, min, sec):
#     # 2. 定义定时器事件
#     def timerEvent(selfs,evt):

class WorkerRunnable(QRunnable):
    def __init__(self):
        super().__init__()

    def run(self):
        # 执行耗时任务
        # MainWindow.checktime

        # 完成后执行回调函数
        QThreadPool.globalInstance().start(self.callback)



    def callback(self):
        # 更新UI
        print("任务已完成")



class QthreadPost(QThread):

    # 自定义信号为str参数类型
    update_date = pyqtSignal(str)
    sid = None
    tid = None
    ts = None
    id = None
    auth = None
    houadd = None
    name = None
    mbenum = None
    timev = None
    tim_str = None
    tim_tow = None
    tim_hhmm = None
    waittime = None
    def run(self):
        while True:
            try:
                self.textout("LADING....")
                if 0:
                    print("发送信息中")
                    if self.sendInfo() == 0:
                        while True:
                            time.sleep(5)
                else:
                    retbuf = self.getHouserInfo()
                    if retbuf == 0:
                        self.sysAgreement()
                        while True:
                            try:
                                print("发送信息中")
                                if self.sendInfo() == 0:
                                    while True:
                                        time.sleep(5)
                                time.sleep(int(self.timev) / 1000)
                            except Exception as e:
                                print("Error: thread send info err ", e)
                                time.sleep(int(self.timev) / 1000)
                    time.sleep(int(self.timev) / 1000)
            except Exception as e:
                print("Error: thread run err ", e)
                time.sleep(int(self.timev) / 1000)

      # while True:
          # #获得当前系统时间
          # data=QDateTime.currentDateTime()
          # #设置时间显示格式
          # curTime=data.toString('yyyy-MM-dd hh:mm:ss dddd')
          # #发射信号
          # self.update_date.emit(str(curTime))
          # #睡眠一秒
          # # time.sleep(1)




    def textout(self, buffer):
        data=QDateTime.currentDateTime()
        #设置时间显示格式
        curTime=data.toString('yyyy-MM-dd hh:mm:ss dddd')
        debug = str(curTime) + ": "+ buffer
        print(debug)
        self.update_date.emit(debug)

    # 处理要做的业务逻辑
    def setDate(self, sid,tid,ts,id,auth,houadd,name,mbenum,timev):  # 专门定义一个方法将主线程的参数传给子线程
        self.sid = sid
        self.tid = tid
        self.ts = ts
        self.id = id
        self.auth = auth
        self.houadd = houadd
        self.name = name
        self.mbenum = mbenum
        self.timev = timev

    def setTimeDate(self, tm_one, tm_tow, hhmm):  # 专门定义一个方法将主线程的参数传给子线程
        self.tim_str = tm_one
        self.tim_tow = tm_tow
        self.tim_hhmm = hhmm


    def sendTime(self):
        inum = 0
        UsrId = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x" + self.id + ")XWEB/9115"
        data = {
            "id": 7,
            "type": 0
        }
        heard = {
            "Connection": "keep-alive",
            "Content-Length": str(12),
            "x-fetch-sid": self.sid,
            "xweb_xhr": str(1),
            "x-fetch-tid": self.tid,
            "x-fetch-ts": self.ts,
            "Authorization": str(self.auth),
            "User-Agent": UsrId,
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Accept": "*/*",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://servicewechat.com/wx750913032d12da97/84/page-frame.html",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        print(data)
        # while True:
        try:
            # js = json.dumps(data)
            # payload = json.loads(js, encoding='utf-8')
            # datas = {"param1": "Detector", "param2": "cnblogs"}
            r = requests.post("https://czgy.xmanju.com:5001/api/sysReserveTime/findReserveTime", headers=heard,data=data, verify=False)
            self.textout(str(r.text))
            print("recv: " + str(r.text))

            try:
                resp = r.json()  # 将返回值转换成字典格式
            except json.decoder.JSONDecodeError as e:
                print("JSONDecodeError:", str(e))
            rcvdatatm = jsonpath.jsonpath(resp, '$.error')  # token的jsonpath表达式：$..token
            if rcvdatatm[0] == "-1":
                self.textout("登录超时。。。。。")
            rcvdatatm = jsonpath.jsonpath(resp, '$.data')  # token的jsonpath表达式：$..token
            if rcvdatatm[0] == "null":
                self.textout("户型还未开放")
                retun -1
            else:
                time1 = jsonpath.jsonpath(resp, '$..month')  # token的jsonpath表达式：$..token
                print(time1)
                time2 = jsonpath.jsonpath(resp, '$..dateList[*]')  # token的jsonpath表达式：$..token
                print(time2)
                time3 = jsonpath.jsonpath(resp, '$..timeList[*]')  # token的jsonpath表达式：$..token
                print(time3)
                timebeij = str(time1[0]) + str(time2[0]) + "日 " + str(time3[0])
                self.textout("时间：")
                self.textout(timebeij)

                time4 = str(time1[0]) + str(time2[0])
                try:
                    timeout = time4.replace("年", "-")
                    timeout2 = timeout.replace("月", "-")

                    print("时间" + timeout2)
                    self.textout(timeout2)
                    self.setTimeDate(timebeij,timeout2,str(time3[0]))
                except Exception as e:
                    print("Error time:", e)
                self.textout("时间状态：")
                self.textout(timeout)

                return 0

            if r.status_code != 200:
                return -1
                # if inum == 5:
                #     return -1
                # inum = inum + 1
            # time.sleep(int(timev) / 1000)
        except Exception as e:
            print("Error time:", e)
            # time.sleep(int(timev) / 1000)

    def getHouserInfo(self):
        data = QDateTime.currentDateTime()
        # 设置时间显示格式
        curTime = data.toString('yyyy-MM-dd hh:mm:ss')
        self.textout(str(curTime))

        UsrId = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x" + self.id + ")XWEB/9115"
        data = {
            "status_EQ": 1,
            "openBeginTime_DATETIMEELT": str(curTime),
            "EXPR_OR": {
                "openEndTime_DATETIMEEGT": str(curTime),
                "openEndTime_EMPTY": "NULL"
            },
            "pageSize": 50
        }
        js = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        print("len:", str(len(data)))

        headers = {
            "Connection": "keep-alive",
            "Content-Length": str(230),
            "x-fetch-sid": self.sid,
            "xweb_xhr": str(1),
            "x-fetch-tid": self.tid,
            "x-fetch-ts": self.ts,
            "Authorization": str(self.auth),
            "User-Agent": UsrId,
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "*/*",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://servicewechat.com/wx750913032d12da97/84/page-frame.html",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

        print(js)
        # js = json.dumps(data)
        # payload = json.loads(js, encoding='utf-8')
        # datas = {"param1": "Detector", "param2": "cnblogs"}
        # r = requests.post("http://www.example.com", headers=headers,
        #                   data=bytes(js, encoding="utf-8"))

        try:
            # requests.adapters.DEFAULT_RETRIES = 2
            # response = requests.post(url, data=body, headers=http_headers, timeout=5)
            r = requests.post("https://czgy.xmanju.com:5001/api/base/sysWaitSetting/listPage", headers=headers,
                          data=bytes(js, encoding="utf-8"), timeout=2)
        except Exception as ee:
            print("get house info:（timeout）", str(ee))
            self.textout("获取房源超时")
            return -1
        # r = requests.post("https://czgy.xmanju.com:5001/api/base/sysWaitSetting/listPage", headers=headers,
        #                   data=bytes(js, encoding="utf-8"), timeout=2)
        print(r.text)
        self.textout("send ok getHouserInfo")

        print(r.status_code)
        try:
            resp = r.json()  # 将返回值转换成字典格式
        except json.decoder.JSONDecodeError as e:
            print("JSONDecodeError:", str(e))
        rcvdatatm = jsonpath.jsonpath(resp, '$.error')  # token的jsonpath表达式：$..token
        if rcvdatatm[0] != 0:
            self.textout("失败")
            return -1
            # self.textout("《《《《《《《《《《《《《《《《《《《预约成功》》》》》》》》》》》》》》》》》》》")
            # self.textout("123456789")


        iInx = jsonpath.jsonpath(resp, '$..data.totalElements')  # token的jsonpath表达式：$..token
        rcvdatatm = jsonpath.jsonpath(resp, '$.data.content[*].houseTypeName')  # token的jsonpath表达式：$..token
        for i in range(iInx[0]):
            if (rcvdatatm[i] == "一房一厅(叩叩·珩琦社区 )") or (rcvdatatm[i] == "一房一厅(叩叩·珩琦社区)"):
            # if rcvdatatm[i] == "三房型(双鲤新城)":
                self.textout("parse(一房一厅(叩叩·珩琦社区 ))")
                recvwaittime = jsonpath.jsonpath(resp, '$.data.content[*].waitTime')  # token的jsonpath表达式：$..token
                self.waittime = recvwaittime[i]
                return 0
            time.sleep(0.1)
        self.textout("unable to parse(一房一厅珩琦社区)")
        return -1

    def getHouserInfo_test(self):
        data = QDateTime.currentDateTime()
        # 设置时间显示格式
        curTime = data.toString('yyyy-MM-dd hh:mm:ss')
        self.textout(str(curTime))

        UsrId = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x" + self.id + ")XWEB/9115"
        data = {
            "status_EQ": 1,
            "openBeginTime_DATETIMEELT": str(curTime),
            "EXPR_OR": {
                "openEndTime_DATETIMEEGT": str(curTime),
                "openEndTime_EMPTY": "NULL"
            },
            "pageSize": 50
        }
        js = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        print("len:", str(len(data)))

        headers = {
            "Connection": "keep-alive",
            "Content-Length": str(230),
            "x-fetch-sid": self.sid,
            "xweb_xhr": str(1),
            "x-fetch-tid": self.tid,
            "x-fetch-ts": self.ts,
            "Authorization": str(self.auth),
            "User-Agent": UsrId,
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "*/*",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://servicewechat.com/wx750913032d12da97/84/page-frame.html",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

        print(js)
        # js = json.dumps(data)
        # payload = json.loads(js, encoding='utf-8')
        # datas = {"param1": "Detector", "param2": "cnblogs"}
        # r = requests.post("http://www.example.com", headers=headers,
        #                   data=bytes(js, encoding="utf-8"))

        try:
            # requests.adapters.DEFAULT_RETRIES = 2
            # response = requests.post(url, data=body, headers=http_headers, timeout=5)
            r = requests.post("https://czgy.xmanju.com:5001/api/base/sysWaitSetting/listPage", headers=headers,
                              data=bytes(js, encoding="utf-8"), timeout=2)
        except Exception as ee:
            print("get house info:（timeout）", str(ee))
            self.textout("获取房源超时")
            return -1
        # r = requests.post("https://czgy.xmanju.com:5001/api/base/sysWaitSetting/listPage", headers=headers,
        #                   data=bytes(js, encoding="utf-8"), timeout=2)
        print(r.text)
        self.textout("send ok getHouserInfo")

        print(r.status_code)
        try:
            resp = r.json()  # 将返回值转换成字典格式
        except json.decoder.JSONDecodeError as e:
            print("JSONDecodeError:", str(e))
        rcvdatatm = jsonpath.jsonpath(resp, '$.error')  # token的jsonpath表达式：$..token
        if rcvdatatm[0] != 0:
            self.textout("失败")
            return -1
            # self.textout("《《《《《《《《《《《《《《《《《《《预约成功》》》》》》》》》》》》》》》》》》》")
            # self.textout("123456789")

        iInx = jsonpath.jsonpath(resp, '$..data.totalElements')  # token的jsonpath表达式：$..token
        rcvdatatm = jsonpath.jsonpath(resp, '$.data.content[*].houseTypeName')  # token的jsonpath表达式：$..token
        for i in range(iInx[0]):
            # if (rcvdatatm[i] == "一房一厅(叩叩·珩琦社区 )") or (rcvdatatm[i] == "一房一厅(叩叩·珩琦社区)"):
            if rcvdatatm[i] == "三房型(双鲤新城)":
                self.textout("parse(三房型(双鲤新城))")
                recvwaittime = jsonpath.jsonpath(resp, '$.data.content[*].waitTime')  # token的jsonpath表达式：$..token
                self.waittime = recvwaittime[i]
                return 0
            time.sleep(0.1)
        self.textout("unable to parse(三房型(双鲤新城))")
        return -1

    def sysAgreement(self):
        UsrId = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x" + self.id + ")XWEB/9115"
        data = {
            "code": "DFSM",
            "projectIds_INSET": [7, 0]
        }
        js = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        print("len:", str(len(data)))

        headers = {
            "Connection": "keep-alive",
            "Content-Length": str(230),
            "x-fetch-sid": self.sid,
            "xweb_xhr": str(1),
            "x-fetch-tid": self.tid,
            "x-fetch-ts": self.ts,
            "Authorization": str(self.auth),
            "User-Agent": UsrId,
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "*/*",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://servicewechat.com/wx750913032d12da97/84/page-frame.html",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        try:
            r = requests.post("https://czgy.xmanju.com:5001/api/sysAgreement/find", headers=headers,
                              data=bytes(js, encoding="utf-8"), timeout=1)
        except Exception as ee:
            print("get afreement:（timeout）", str(ee))
            self.textout("获取户型超时")
            return -1

        print(r.text)
        self.textout("send ok sysAgreement")


    def sendInfo(self):
        if NEWPOST:
            UsrId = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x" + self.id + ")XWEB/9115"
            data = {
                "type": 1,
                "waitTime": self.waittime,
                "mobile": self.mbenum,
                "renterId": 38358,
                "name": self.name,
                "projectName": "叩叩·珩琦社区 ",
                "houseTypeName": "一房一厅",
                "projectId": 7,
                "houseTypeId": 15
            }

            data1 = {
                "type": 1,
                "waitTime": 24,
                "mobile": self.mbenum,
                "renterId": 38358,
                "name": self.name,
                "projectName": "叩叩·园博社区",
                "houseTypeName": "一房一厅",
                "projectId": 6,
                "houseTypeId": 13
            }
            data2 = {
                "type": 1,
                "waitTime": 24,
                "mobile": self.mbenum,
                "renterId": 38358,
                "name": self.name,
                "projectName": "双鲤新城",
                "houseTypeName": "三房型",
                "projectId": 16,
                "houseTypeId": 38
            }
            js = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
            print("len:", str(len(data)))

            headers = {
                "Connection": "keep-alive",
                "Content-Length": str(230),
                "x-fetch-sid": self.sid,
                "xweb_xhr": str(1),
                "x-fetch-tid": self.tid,
                "x-fetch-ts": self.ts,
                "Authorization": str(self.auth),
                "User-Agent": UsrId,
                "Content-Type": "application/json;charset=UTF-8",
                "Accept": "*/*",
                "Sec-Fetch-Site": "cross-site",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://servicewechat.com/wx750913032d12da97/84/page-frame.html",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
            }

            print(js)
            # js = json.dumps(data)
            # payload = json.loads(js, encoding='utf-8')
            # datas = {"param1": "Detector", "param2": "cnblogs"}
            # r = requests.post("http://www.example.com", headers=headers,
            #                   data=bytes(js, encoding="utf-8"))

            try:
                r = requests.post("https://czgy.xmanju.com:5001/api/rntWaitRoom/add", headers=headers,
                                  data=bytes(js, encoding="utf-8"), timeout=1)
            except Exception as ee:
                print("add msg:（timeout）", str(ee))
                self.textout("抢房超时")
                return -1

            print(r.text)
            self.textout("send ok sendInfo")

            try:
                resp = r.json()  # 将返回值转换成字典格式
            except json.decoder.JSONDecodeError as e:
                print("JSONDecodeError:", str(e))
            rcvdatatm = jsonpath.jsonpath(resp, '$.error')  # token的jsonpath表达式：$..token
            if rcvdatatm[0] != 0:
                self.textout("失败")
                return -1

            else:
                self.textout("《《《《《《《《《《抢房成功》》》》》》》》》")
                return 0


        else:
            # json_data = '{"mobile":"15759816561","name":"黄东波","visitTime":"2023年11月18日 14:00-18:00","channelId":null,"visitDate":"2023-11-18","projectName":"叩叩·杏锦店","visitTimeQuantum":"14:00-18:00","renterId":38358,"projectId":"93"}'
            # data0 = json.loads(json_data)
            # data = json.dumps(data0)
            UsrId = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x" + self.id + ")XWEB/9115"
            data = {
                "mobile": self.mbenum,
                "name": self.name,
                "visitTime": self.tim_str,
                "channelId": None,
                "visitDate": self.tim_tow,
                "projectName": self.houadd,
                "visitTimeQuantum": self.tim_hhmm,
                "renterId": 38358,
                "projectId": "7"
            }
            js = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
            print("len:", str(len(data)))

            headers = {
                "Connection": "keep-alive",
                "Content-Length": str(230),
                "x-fetch-sid": self.sid,
                "xweb_xhr": str(1),
                "x-fetch-tid": self.tid,
                "x-fetch-ts": self.ts,
                "Authorization": str(self.auth),
                "User-Agent": UsrId,
                "Content-Type": "application/json;charset=UTF-8",
                "Accept": "*/*",
                "Sec-Fetch-Site": "cross-site",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://servicewechat.com/wx750913032d12da97/84/page-frame.html",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
            }

            print(js)
            # js = json.dumps(data)
            # payload = json.loads(js, encoding='utf-8')
            # datas = {"param1": "Detector", "param2": "cnblogs"}
            r = requests.post("https://czgy.xmanju.com:5001/api/sys/rntAppointment/add", headers=headers, data=bytes(js, encoding="utf-8"))
            print(r.text)

            print(r.status_code)
            try:
                resp = r.json()  # 将返回值转换成字典格式
            except json.decoder.JSONDecodeError as e:
                print("JSONDecodeError:", str(e))
            rcvdatatm = jsonpath.jsonpath(resp, '$.error')  # token的jsonpath表达式：$..token
            if rcvdatatm[0] == "0":
                self.textout("《《《《《《《《《《《《《《《《《《《预约成功》》》》》》》》》》》》》》》》》》》")
                self.textout("123456789")
                return 0
            else:
                return -1

    def sendInfo_test(self):
        if NEWPOST:
            UsrId = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x" + self.id + ")XWEB/9115"
            data = {
                "type": 1,
                "waitTime": self.waittime,
                "mobile": self.mbenum,
                "renterId": 38358,
                "name": self.name,
                "projectName": "叩叩·珩琦社区 ",
                "houseTypeName": "一房一厅",
                "projectId": 7,
                "houseTypeId": 15
            }

            data1 = {
                "type": 1,
                "waitTime": 24,
                "mobile": self.mbenum,
                "renterId": 38358,
                "name": self.name,
                "projectName": "叩叩·园博社区",
                "houseTypeName": "一房一厅",
                "projectId": 6,
                "houseTypeId": 13
            }
            data2 = {
                "type": 1,
                "waitTime": 24,
                "mobile": self.mbenum,
                "renterId": 38358,
                "name": self.name,
                "projectName": "双鲤新城",
                "houseTypeName": "三房型",
                "projectId": 16,
                "houseTypeId": 38
            }
            js = json.dumps(data2, separators=(',', ':'), ensure_ascii=False)
            print("len:", str(len(data2)))

            headers = {
                "Connection": "keep-alive",
                "Content-Length": str(230),
                "x-fetch-sid": self.sid,
                "xweb_xhr": str(1),
                "x-fetch-tid": self.tid,
                "x-fetch-ts": self.ts,
                "Authorization": str(self.auth),
                "User-Agent": UsrId,
                "Content-Type": "application/json;charset=UTF-8",
                "Accept": "*/*",
                "Sec-Fetch-Site": "cross-site",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://servicewechat.com/wx750913032d12da97/84/page-frame.html",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
            }

            print(js)
            # js = json.dumps(data)
            # payload = json.loads(js, encoding='utf-8')
            # datas = {"param1": "Detector", "param2": "cnblogs"}
            # r = requests.post("http://www.example.com", headers=headers,
            #                   data=bytes(js, encoding="utf-8"))

            try:
                r = requests.post("https://czgy.xmanju.com:5001/api/rntWaitRoom/add", headers=headers,
                                  data=bytes(js, encoding="utf-8"), timeout=1)
            except Exception as ee:
                print("add msg:（timeout）", str(ee))
                self.textout("抢房超时")
                return -1

            print(r.text)
            self.textout("send ok sendInfo")

            try:
                resp = r.json()  # 将返回值转换成字典格式
            except json.decoder.JSONDecodeError as e:
                print("JSONDecodeError:", str(e))
            rcvdatatm = jsonpath.jsonpath(resp, '$.error')  # token的jsonpath表达式：$..token
            if rcvdatatm[0] != 0:
                self.textout("失败")
                return -1

            else:
                self.textout("《《《《《《《《《《抢房成功》》》》》》》》》")
                return 0


        else:
            # json_data = '{"mobile":"15759816561","name":"黄东波","visitTime":"2023年11月18日 14:00-18:00","channelId":null,"visitDate":"2023-11-18","projectName":"叩叩·杏锦店","visitTimeQuantum":"14:00-18:00","renterId":38358,"projectId":"93"}'
            # data0 = json.loads(json_data)
            # data = json.dumps(data0)
            UsrId = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x" + self.id + ")XWEB/9115"
            data = {
                "mobile": self.mbenum,
                "name": self.name,
                "visitTime": self.tim_str,
                "channelId": None,
                "visitDate": self.tim_tow,
                "projectName": self.houadd,
                "visitTimeQuantum": self.tim_hhmm,
                "renterId": 38358,
                "projectId": "7"
            }
            js = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
            print("len:", str(len(data)))

            headers = {
                "Connection": "keep-alive",
                "Content-Length": str(230),
                "x-fetch-sid": self.sid,
                "xweb_xhr": str(1),
                "x-fetch-tid": self.tid,
                "x-fetch-ts": self.ts,
                "Authorization": str(self.auth),
                "User-Agent": UsrId,
                "Content-Type": "application/json;charset=UTF-8",
                "Accept": "*/*",
                "Sec-Fetch-Site": "cross-site",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://servicewechat.com/wx750913032d12da97/84/page-frame.html",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
            }

            print(js)
            # js = json.dumps(data)
            # payload = json.loads(js, encoding='utf-8')
            # datas = {"param1": "Detector", "param2": "cnblogs"}
            r = requests.post("https://czgy.xmanju.com:5001/api/sys/rntAppointment/add", headers=headers, data=bytes(js, encoding="utf-8"))
            print(r.text)

            print(r.status_code)
            try:
                resp = r.json()  # 将返回值转换成字典格式
            except json.decoder.JSONDecodeError as e:
                print("JSONDecodeError:", str(e))
            rcvdatatm = jsonpath.jsonpath(resp, '$.error')  # token的jsonpath表达式：$..token
            if rcvdatatm[0] == "0":
                self.textout("《《《《《《《《《《《《《《《《《《《预约成功》》》》》》》》》》》》》》》》》》》")
                self.textout("123456789")
                return 0
            else:
                return -1



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.thread_pool = QThreadPool.globalInstance()
        self.thread_pool.setMaxThreadCount(1)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

        # self.thread_obj = 0
        self.setupUi(self)
        self.demo()


    @property
    def checktime(self):

        def textout(*args):
            self.textOut.append(args[0])  # 文本框逐条添加数据
            self.textOut.moveCursor(self.textOut.textCursor().End)  # 文本框显示到底部
            time.sleep(0.2)

        time_beg = self.timeEdit_beg.time()
        print(time_beg.toString('hh:mm:ss'))  # 返回字符串 '12:34:56'
        # print(time_beg.hour())
        # print(time_beg.minute())
        # print(time_beg.second())

        hour_beg = time_beg.hour()
        min_beg = time_beg.minute()
        sec_beg = time_beg.second()

        time_end = self.timeEdit_end.time()
        print(time_end.toString('hh:mm:ss'))  # 返回字符串 '12:34:56'
        hour_end = time_beg.hour()
        min_end = time_beg.minute()
        sec_end = time_beg.second()

        current_time = QDateTime.currentDateTime()
        print(current_time.toString("yyyy-MM-dd hh:mm:ss"))
        hour_now = current_time.time().hour()
        min_now = current_time.time().minute()
        sec_now = current_time.time().second()

        if hour_beg <= hour_end and min_beg <= min_end and sec_beg <= sec_end:
            tm_beg = datetime.time(hour_beg, min_beg, sec_beg)
            tm_end = datetime.time(hour_end, min_end, sec_end)
            tm_now = datetime.time(hour_now, min_now, sec_now)
            if tm_beg <= tm_now <= tm_end:
                textout("时间区间正常启动中...")
                return 1
            elif tm_now <= tm_beg:
                return 2

        textout("时间设置错误，请重新设置......")
        return 0

    def demo(self):
        """
        本节课所有的控件都在此函数里进行演示
        """

        def _async_raise(tid, exctype):
            """raises the exception, performs cleanup if needed"""
            tid = ctypes.c_long(tid)
            if not inspect.isclass(exctype):
                exctype = type(exctype)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
            if res == 0:
                raise ValueError("invalid thread id")
            elif res != 1:
                # """if it returns a number greater than one, you're in trouble,
                # and you should call it again with exc=NULL to revert the effect"""
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")

        def stop_thread(thread):
            _async_raise(thread.ident, SystemExit)

        def thread_Post(sid,tid,ts,id,auth,houadd,name,mbenum,timev):
            if sid == "0" and tid == "0" and ts == "0" and id == "0" and auth == "0" and houadd == "0" and name == "0" and mbenum == "0" and timev == "0":
            # if sid == "" or tid == "" or ts == "" or id == "" or auth == "" or houadd == "" or name == "" or mbenum == "" or timeval == "":
                while True:
                    print("无内容....")
                    time.sleep(2)
            while True:
                # iret = checktime()
                # if  iret == 1:
                #     print("a=%d,b=%d,c=%d" % (a, b, c))
                # elif iret == 2:
                #     textout("定时中....")
                #     time.sleep(60)
                # else:
                #     textout("时间不在范围内")
                #     while True:
                #         time.sleep(60)
                try:
                    textout("LADING....")
                    retbuf = sendTime(sid,tid,ts,id,auth,timev)

                    time.sleep(int(timev) / 1000)
                except Exception as e:
                    print("Error: thread run err ", e)
                    time.sleep(int(timev) / 1000)





        def start_task():
            runnable = WorkerRunnable()
            self.thread_pool.start(runnable)

        def textout(*args):
            self.textOut.append(args[0])  # 文本框逐条添加数据
            self.textOut.moveCursor(self.textOut.textCursor().End)  # 文本框显示到底部
            time.sleep(0.2)



        def BCheck_beg(*args):
            # print("foo被执行了, 带的数据是", args) # 配合按钮API clicked、toggled使用
            # if self.pushButton_begin.isChecked() == True:
            textout("预约开始...")
            self.pushButton_begin.setCheckable(False)
            self.pushButton_begin.setEnabled(False)
            self.pushButton_stop.setEnabled(True)
            self.pushButton_stop.setCheckable(True)
            self.pushButton_over.setCheckable(True)
            self.pushButton_over.setEnabled(True)
            usr_len = getlen()
            usr_ts = getts()
            usr_sid = getlsid()
            usr_tid = getltid()
            usr_auth = getauth()
            usr_id = getlId()
            usr_time = getltimer()
            usr_moble = getmoble()
            usr_name = getusrname()
            usr_addr = gethouseaddr()


            if usr_len == "" or usr_ts == "" or usr_sid == "" or usr_tid == "" or usr_auth == "" or usr_id == "" or usr_time == "" or usr_moble == "" or usr_name == "" or usr_addr == "":
                textout("信息填写不完整，请设置完整后再开始......")
                BCheck_end()
            else:

                self.threadpost.start()
                self.threadpost.setDate(usr_sid,usr_tid,usr_ts,usr_id,usr_auth,usr_addr,usr_name,usr_moble,usr_time)
                textout("信息填写完整，开始抢房......")
                save_info()

                # self.thread_obj = threading.Thread(target=thread_Post, args=(usr_sid,usr_tid,usr_ts,usr_id,usr_auth,usr_addr,usr_name,usr_moble,usr_time))
                # self.thread_obj.start()


                # start_task()





                    # threading.Thread(target=_slot1, args=(self.textBrowser, self.lineEdit)).start()

        def BCheck_stop(*args):
            # if self.pushButton_stop.isChecked() == True:
            textout("预约暂停...")
            self.pushButton_stop.setCheckable(False)
            self.pushButton_stop.setEnabled(False)
            self.pushButton_begin.setEnabled(True)
            self.pushButton_begin.setCheckable(True)
            self.pushButton_over.setCheckable(True)
            self.pushButton_over.setEnabled(True)
            # if self.thread_obj.is_alive():
            #     stop_thread(self.thread_obj)
            if self.threadpost.isRunning():
                self.threadpost.terminate()
                self.threadpost.wait()





        def BCheck_end(*args):
            # if self.pushButton_over.isChecked() == True:
            textout("预约结束...")
            self.pushButton_over.setCheckable(False)
            self.pushButton_over.setEnabled(False)
            self.pushButton_begin.setEnabled(True)
            self.pushButton_begin.setCheckable(True)
            self.pushButton_stop.setEnabled(False)
            self.pushButton_stop.setCheckable(False)
            # if self.thread_obj.is_alive():
            #     stop_thread(self.thread_obj)
            if self.threadpost.isRunning():
                self.threadpost.terminate()
                self.threadpost.wait()



        def getlen():
            len = self.lineEdit_Len.text()
            buf = "len：" + len
            textout(buf)
            return len


        def getlsid():
            sid = self.lineEdit_sid.text()
            buf = "sid：" + sid
            textout(buf)
            return sid


        def getltid():
            tid = self.lineEdit_tid.text()
            buf = "sid：" + tid
            textout(buf)
            return tid


        def getts():
            ts = self.lineEdit_ts.text()
            buf = "ts：" + ts
            textout(buf)
            return ts


        def getauth():
            lineauth = self.lineEdit_auth.text()
            buf = "auth：" + lineauth
            textout(buf)
            return lineauth


        def getlId():
            Id = self.lineEdit_Id.text()
            buf = "Id：" + Id
            textout(buf)
            return Id

        def getmoble():
            moble = self.lineEdit_mobile.text()
            buf = "moble：" + moble
            textout(buf)
            return moble

        def getusrname():
            name = self.lineEdit_name.text()
            buf = "name：" + name
            textout(buf)
            return name

        def gethouseaddr():
            addr = self.lineEdit_addr.text()
            buf = "addr：" + addr
            textout(buf)
            return addr


        def getltimer():
            timer = self.lineEdi_timer.text()
            timems =  timer
            unit = "ms"
            if self.radioButton_min.isChecked():
                unit = "min"
            elif self.radioButton_us.isChecked():
                unit =  "us"
            elif self.radioButton_ms.isChecked():
                unit =  "ms"
            elif self.radioButton_s.isChecked():
                unit =  "s"
                timems = timer * 1000
            else:
                unit = "ms"

            buf = "TIMER：" + timer + unit + "(" + timems + "ms" + ")"
            textout(buf)
            return timems

        def checktime():

            time_beg = self.timeEdit_beg.time()
            print(time_beg.toString('hh:mm:ss'))  # 返回字符串 '12:34:56'
            # print(time_beg.hour())
            # print(time_beg.minute())
            # print(time_beg.second())

            hour_beg = time_beg.hour()
            min_beg = time_beg.minute()
            sec_beg = time_beg.second()

            time_end = self.timeEdit_end.time()
            print(time_end.toString('hh:mm:ss'))  # 返回字符串 '12:34:56'
            hour_end = time_beg.hour()
            min_end = time_beg.minute()
            sec_end = time_beg.second()

            # current_time = time.localtime()
            # # print(current_time.totoString("hh:mm:ss"))
            # hour_now = current_time.tm_hour
            # min_now = current_time.tm_min
            # sec_now = current_time.tm_sec
            #
            tm_beg = datetime.time(hour_beg, min_beg, sec_beg)
            tm_end = datetime.time(hour_end, min_end, sec_end)
            # tm_now = datetime.time(hour_now, min_now, sec_now)

            if tm_beg < tm_end:
                # if tm_beg < tm_now < tm_end:
                #     textout("时间区间正常启动中...")
                return 1
                # elif tm_now < tm_beg:
                #     return 2

            textout("时间设置错误，请重新设置......")
            return 0

        def sendInfo():
            # json_data = '{"mobile":"15759816561","name":"黄东波","visitTime":"2023年11月18日 14:00-18:00","channelId":null,"visitDate":"2023-11-18","projectName":"叩叩·杏锦店","visitTimeQuantum":"14:00-18:00","renterId":38358,"projectId":"93"}'
            # data0 = json.loads(json_data)
            # data = json.dumps(data0)
            data = {
                "mobile": "11223344556",
                "name": "梅兰芳",
                "visitTime": "2023年11月25日 14:00-18:00",
                "channelId": None,
                "visitDate": "2023-11-26",
                "projectName": "钉钉·李白歌",
                "visitTimeQuantum": "14:00-18:00",
                "renterId": 38358,
                "projectId": "93"
            }
            js = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
            print("len:", str(len(data)))


            headers = {
                "Content-Type": "application/json; charset=UTF-8",  # 设置消息头参数
                "Authorization": "Bearer token123",  # 设置消息头参数
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Content-Length": str(230)

            }

            print(js)
            # js = json.dumps(data)
            # payload = json.loads(js, encoding='utf-8')
            # datas = {"param1": "Detector", "param2": "cnblogs"}
            r = requests.post("http://httpbin.org/post", headers=headers, data=bytes(js,encoding="utf-8"))

            print(r.text)

            print(r.status_code)


        def sendTime(sid,tid,ts,id,auth,timev):
            inum = 0
            UsrId = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x" + id + ")XWEB/9115"
            data = {
                "id": 93,
                "type": 0
            }
            heard = {
                "Connection": "keep-alive",
                "Content-Length": str(12),
                "x-fetch-sid": sid,
                "xweb_xhr": str(1),
                "x-fetch-tid": tid,
                "x-fetch-ts": ts,
                "Authorization": auth,
                "User-Agent": UsrId,
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "Accept": "*/*",
                "Sec-Fetch-Site": "cross-site",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://servicewechat.com/wx750913032d12da97/84/page-frame.html",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
            }
            print(data)
            while True:
                try:
                    # js = json.dumps(data)
                    # payload = json.loads(js, encoding='utf-8')
                    # datas = {"param1": "Detector", "param2": "cnblogs"}
                    r = requests.post("https://czgy.xmanju.com:5001/api/sysReserveTime/findReserveTime", headers = heard, data=data, verify=False)
                    textout(str(r.text))
                    print("recv: " + str(r.text))

                    resp = r.json()  # 将返回值转换成字典格式
                    rcvdatatm = jsonpath.jsonpath(resp, '$.data')  # token的jsonpath表达式：$..token
                    if rcvdatatm[0] == "null":
                        textout("户型还未开放")
                        # return None
                    else:
                        time1 = jsonpath.jsonpath(resp, '$..month')  # token的jsonpath表达式：$..token
                        print(time1)
                        time2 = jsonpath.jsonpath(resp, '$..dateList[*]')  # token的jsonpath表达式：$..token
                        print(time2)
                        time3 = jsonpath.jsonpath(resp, '$..timeList[*]')  # token的jsonpath表达式：$..token
                        print(time3)
                        timebeij = str(time1[0]) + str(time2[0]) + "日 " + str(time3[0])
                        textout("时间：")
                        textout(timebeij)
                        # return time

                    if r.status_code != 200:
                        return -1
                        # if inum == 5:
                        #     return -1
                        # inum = inum + 1
                    time.sleep(int(timev) / 1000)
                except Exception as e:
                    print("Error:", e)
                    time.sleep(int(timev) / 1000)

        def save_info():
            settings = QSettings("./config.ini", QSettings.IniFormat)
            settings.setValue("ts", self.lineEdit_ts.text())
            settings.setValue("tid", self.lineEdit_tid.text())
            settings.setValue("addr", self.lineEdit_addr.text())
            settings.setValue("name", self.lineEdit_name.text())
            settings.setValue("mobile", self.lineEdit_mobile.text())
            settings.setValue("auth", self.lineEdit_auth.text())
            settings.setValue("Id", self.lineEdit_Id.text())
            settings.setValue("Len", self.lineEdit_Len.text())
            settings.setValue("sid", self.lineEdit_sid.text())



        ##显示上次保存的值
        def init_info():
            if os.path.exists("./config.ini") == True:
                settings = QSettings("./config.ini", QSettings.IniFormat)
                the_ts = settings.value("ts")
                the_tid = settings.value("tid")
                the_addr = settings.value("addr")
                the_name = settings.value("name")
                the_mobile = settings.value("mobile")
                the_auth = settings.value("auth")
                the_Id = settings.value("Id")
                the_Len = settings.value("Len")
                the_sid = settings.value("sid")


                self.lineEdit_Len.setText(the_Len)
                self.lineEdit_sid.setText(the_sid)
                self.lineEdit_Id.setText(the_Id)
                self.lineEdit_auth.setText(the_auth)
                self.lineEdit_tid.setText(the_tid)
                self.lineEdit_mobile.setText(the_mobile)
                self.lineEdit_name.setText(the_name)
                self.lineEdit_addr.setText(the_addr)
                self.lineEdit_ts.setText(the_ts)

        def getHouserInfo():
            # UsrId = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x" + self.id + ")XWEB/9115"
            data = {

                "status_EQ": 1,
                "openBeginTime_DATETIMEELT": "2024-02-01 10:00:08",
                "EXPR_OR": {
                    "openEndTime_DATETIMEEGT": "2024-02-01 10:00:08",
                    "openEndTime_EMPTY": "NULL"
                },
                "pageSize": 50
            }
            js = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
            print("len:", str(len(data)))

            headers = {
                # "Connection": "keep-alive",
                # "Content-Length": str(230),
                # "x-fetch-sid": self.sid,
                # "xweb_xhr": str(1),
                # "x-fetch-tid": self.tid,
                # "x-fetch-ts": self.ts,
                # "Authorization": str(self.auth),
                # "User-Agent": UsrId,
                # "Content-Type": "application/json;charset=UTF-8",
                # "Accept": "*/*",
                # "Sec-Fetch-Site": "cross-site",
                # "Sec-Fetch-Mode": "cors",
                # "Sec-Fetch-Dest": "empty",
                # "Referer": "https://servicewechat.com/wx750913032d12da97/84/page-frame.html",
                # "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
            }

            print(js)
            # js = json.dumps(data)
            # payload = json.loads(js, encoding='utf-8')
            # datas = {"param1": "Detector", "param2": "cnblogs"}
            r = requests.post("http://www.example.com", headers = headers,
                              data=bytes(js, encoding="utf-8"))
            print(r.text)
            textout(str(r.text))

            # print(r.status_code)
            # try:
            #     resp = r.json()  # 将返回值转换成字典格式
            # except json.decoder.JSONDecodeError as e:
            #     print("JSONDecodeError:", str(e))
            # rcvdatatm = jsonpath.jsonpath(resp, '$.error')  # token的jsonpath表达式：$..token
            # if rcvdatatm[0] == "0":
            #     self.textout("《《《《《《《《《《《《《《《《《《《预约成功》》》》》》》》》》》》》》》》》》》")
            #     self.textout("123456789")
            #     return 0
            # else:
            #     return -1





        # self.pushButton_begin.setCheckable(True)
        # self.pushButton_begin.setAutoRepeat(True)  # 设置长按时重复执行任务
        # print(self.pushButton_begin.isChecked())  # 提示按钮是否已按下

        # self.pushButton_begin.pressed.connect(BCheck_beg)  # 当鼠标指针在按钮上并按下左键时执行foo
        # self.pushButton_begin.released.connect(BCheck_beg)  # 当鼠标左键被释放时执行foo
        # self.pushButton_begin.clicked.connect(BCheck_beg)  # 当鼠标左键被按下然后释放时，或者快捷键被释放时执行foo
        # self.pushButton_begin.toggled.connect(BCheck_beg)  # 当按钮的标记状态发生改变时执行foo

        self.pushButton_begin.setCheckable(True)
        print(self.pushButton_begin.isChecked())  # 提示按钮是否已按下
        self.pushButton_begin.released.connect(BCheck_beg)  # 当鼠标左键被释放时执行foo

        # self.pushButton_stop.setCheckable(True)
        self.pushButton_stop.setEnabled(False)
        print(self.pushButton_stop.isChecked())  # 提示按钮是否已按下
        self.pushButton_stop.released.connect(BCheck_stop)  # 当鼠标左键被释放时执行foo

        # self.pushButton_over.setCheckable(True)
        self.pushButton_over.setEnabled(False)
        print(self.pushButton_over.isChecked())  # 提示按钮是否已按下
        self.pushButton_over.released.connect(BCheck_end)  # 当鼠标左键被释放时执行foo



        # self.lineEdit_Len.setText("Hello World")  # 设置文字
        # self.lineEdit_Len.setEchoMode(QtWidgets.QLineEdit.Normal)  # 设置文本框的显示格式
        #  QLineEdit.Normal 正常显示所输入的字符，此为默认选项
        #  QLineEdit.NoEcho 不显示任何输入的字符，常用于密码类型的输入，且长度保密
        #  QLineEdit.Password 显示与平台相关的密码掩饰字符
        #  QLineEdit.PasswordEchoOnEdit 在编辑时显示字符，负责显示密码类型的输入

        # self.lineEdit_Len.setClearButtonEnabled(True)  # 在编辑框右边加入一个清空按钮
        # self.lineEdit_Len.setMaxLength(10)  # 设置所允许输入的最大字符数为10
        # self.lineEdit_Len.setReadOnly(True)  # 设置只读    False取消只读

        # self.lineEdit_Len.setFocus()  # 获取焦点
        # self.lineEdit_Len.selectAll()  # 全选

        # self.lineEdit_Len.editingFinished.connect(foo)  # 按下返回或回车键或线条编辑失去焦点时 执行foo
        # self.lineEdit_Len.returnPressed.connect(foo)  # 按下返回或回车键时 执行foo
        # self.lineEdit_Len.textChanged.connect(foo)  # 只要文字发生变化就会 执行foo, 包括setText()
        # self.lineEdit_Len.textEdited.connect(foo)  # 无论何时编辑文本都会 执行foo, 不包括setText()

        self.lineEdit_Len.setEchoMode(QtWidgets.QLineEdit.Normal)  # 设置文本框的显示格式
        self.lineEdit_Len.setClearButtonEnabled(True)  # 在编辑框右边加入一个清空按钮

        self.lineEdit_tid.setEchoMode(QtWidgets.QLineEdit.Normal)  # 设置文本框的显示格式
        self.lineEdit_tid.setClearButtonEnabled(True)  # 在编辑框右边加入一个清空按钮

        self.lineEdit_sid.setEchoMode(QtWidgets.QLineEdit.Normal)  # 设置文本框的显示格式
        self.lineEdit_sid.setClearButtonEnabled(True)  # 在编辑框右边加入一个清空按钮

        self.lineEdit_Id.setEchoMode(QtWidgets.QLineEdit.Normal)  # 设置文本框的显示格式
        self.lineEdit_Id.setClearButtonEnabled(True)  # 在编辑框右边加入一个清空按钮

        self.lineEdit_auth.setEchoMode(QtWidgets.QLineEdit.Normal)  # 设置文本框的显示格式
        self.lineEdit_auth.setClearButtonEnabled(True)  # 在编辑框右边加入一个清空按钮

        self.lineEdit_ts.setEchoMode(QtWidgets.QLineEdit.Normal)  # 设置文本框的显示格式
        self.lineEdit_ts.setClearButtonEnabled(True)  # 在编辑框右边加入一个清空按钮

        self.lineEdit_mobile.setEchoMode(QtWidgets.QLineEdit.Normal)  # 设置文本框的显示格式
        self.lineEdit_mobile.setClearButtonEnabled(True)  # 在编辑框右边加入一个清空按钮

        self.lineEdit_name.setEchoMode(QtWidgets.QLineEdit.Normal)  # 设置文本框的显示格式
        self.lineEdit_name.setClearButtonEnabled(True)  # 在编辑框右边加入一个清空按钮

        self.lineEdit_addr.setEchoMode(QtWidgets.QLineEdit.Normal)  # 设置文本框的显示格式
        self.lineEdit_addr.setClearButtonEnabled(True)  # 在编辑框右边加入一个清空按钮

        self.radioButton_ms.setChecked(True)

        # self.thread_obj = threading.Thread(target=thread_Post, args=("0","0","0","0","0","0","0","0","0"))
        # self.thread_obj.start()
        # if self.thread_obj.is_alive():
        #     stop_thread(self.thread_obj)

        self.threadpost = QthreadPost()
        # 信号连接到界面显示槽函数
        self.threadpost.update_date.connect(textout)
        # 多线程开始

        init_info()
        # getHouserInfo()

        # self.showMaximized()


        # sendInfo()



        pass







# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


