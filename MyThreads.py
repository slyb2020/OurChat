from six.moves import _thread
from ID_DEFINE import *
import MySQL
import time
import wx.lib.newevent

(UpdateNewMessagesEvent, EVT_UPDATE_NEWMESSAGES) = wx.lib.newevent.NewEvent()
(UpdateMiddlePanelEvent, EVT_UPDATE_MIDDLEPANEL) = wx.lib.newevent.NewEvent()
(KickOutEvent, Evt_KICKOUT) = wx.lib.newevent.NewEvent()


class UpdateMiddlePanelThread:  # ReadNewMessagesThread:
    def __init__(self, win):
        self.win = win
        self.running = False
        self.myId = 0
        self.friendId = 0
        self.keepGoing = False

    def Start(self, myId, friendId):
        self.myId = myId
        self.friendId = friendId
        if not self.running:
            self.keepGoing = self.running = True
            _thread.start_new_thread(self.Run, ())

    def Stop(self):
        self.keepGoing = False
        while self.running:
            time.sleep(0.05)

    def IsRunning(self):
        return self.running

    def Run(self):
        ourchatDB = MySQL.OurchatDB()
        error, friendId, num, lastMessage, lastTime = ourchatDB.GetFriendMessageOutlook(self.myId, self.friendId)
        if error == ID_NO_ERROR:
            evt = UpdateMiddlePanelEvent(num=num, lastMessage=lastMessage, lastTime=lastTime)
            wx.PostEvent(self.win, evt)
        self.running = False


class ReadNewMessagesThread:
    def __init__(self, win, lastId=0, userId=0, objectUserId=0):
        self.win = win
        self.lastId = lastId
        self.myId = userId
        self.objectUserId = objectUserId
        self.keepGoing = False
        self.running = False
        self.messageList = []

    def Start(self, lastId, myId, objectUserId):
        self.lastId = lastId
        self.myId = myId
        self.objectUserId = objectUserId
        if not self.keepGoing:
            self.keepGoing = self.running = True
            _thread.start_new_thread(self.Run, ())

    def Stop(self):
        self.keepGoing = False
        while self.running:
            time.sleep(0.05)

    def IsRunning(self):
        return self.running

    def Run(self):
        if self.objectUserId == 0:
            self.keepGoing = False
        while self.keepGoing:
            ourchatDB = MySQL.OurchatDB()
            error, newdata = ourchatDB.ReadNewMessages(self.lastId, self.myId, self.objectUserId)
            if error == ID_NO_ERROR:
                if len(newdata) > 0:
                    for message in newdata:
                        self.messageList.append(message)
                    evt = UpdateNewMessagesEvent(newMessages=self.messageList)
                    self.messageList = []
                    wx.PostEvent(self.win, evt)
                ourchatDB = MySQL.OurchatDB()
                error = ourchatDB.UpdateMessagesHaveRead(self.myId, self.objectUserId)
            self.keepGoing = False  # 只读一次数据库，不管读没读到新消息都要Stop进程，等待下次（几秒后）主程序再次Start进程
        self.running = False


class KickOutThread:
    def __init__(self, win, myId, cpuId):
        self.win = win
        self.myId = myId
        self.cpuId = cpuId
        self.keepGoing = False
        self.running = False

    def Start(self, myId, cpuId):
        self.myId = myId
        self.cpuId = cpuId
        if not self.keepGoing:
            self.keepGoing = self.running = True
            _thread.start_new_thread(self.Run, ())

    def Stop(self):
        self.keepGoing = False
        while self.running:
            time.sleep(0.05)

    def IsRunning(self):
        return self.running

    def Run(self):
        while self.keepGoing:
            ourchatDB = MySQL.OurchatDB()
            error, cpuId = ourchatDB.GetCPUId(self.myId)
            if error == ID_NO_ERROR:
                if cpuId != self.cpuId:
                    evt = KickOutEvent(newCPUId=cpuId)
                    wx.PostEvent(self.win, evt)
            self.keepGoing = False  # 只读一次数据库，不管读没读到新消息都要Stop进程，等待下次（几秒后）主程序再次Start进程
        self.running = False
