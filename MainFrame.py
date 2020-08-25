#!/usr/bin/env python
# _*_ coding: UTF-8 _*_
import base64
import wx.adv
from wx.lib.wordwrap import wordwrap
from wmi import WMI
import images
from CheckinDialog import CheckinDialog
from MyConfig import MainConfig
from MyThreads import *


class MainFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self.AdjustSize(size)
        self.InitParameter()
        self.SetIcon(images.Pencil.GetIcon())
        self.mainConfig = MainConfig('setup.cfg')
        isSuccess, self.exId, self.exIdTIP, self.exUserList, self.exUserListTIP = self.mainConfig.GetValue()
        if not isSuccess:
            pass  # 应该有个写记录的操作
        self.GetUserInfo()
        self.CreateMyMenuBar()
        self.SetMenuBar(self.checkoutMENUBAR)
        self.CreateMyStatusBar()
        self.BindEvent()

    def GetUserInfo(self):
        ourchatDB = MySQL.OurchatDB()
        error, data = ourchatDB.GetUserInfo()
        if error == ID_NO_ERROR:
            self.idList = []
            self.nicknameList = []
            self.userList = []
            self.passwordList = []
            self.iconList = []
            for record in data:
                self.idList.append(record[0])
                self.nicknameList.append(record[1])
                self.userList.append(record[2])
                self.passwordList.append(record[3])
                self.iconList.append(record[4])
        else:
            wx.MessageBox("无法打开用户信息数据库，登录失败！")

    def BindEvent(self):
        self.Bind(wx.EVT_MENU, self.OnCheckin, id=ID_CHECKIN)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_HELP)
        self.Bind(wx.EVT_MENU, self.OnCheckout, id=ID_CHECKOUT)
        self.Bind(wx.EVT_MENU, self.OnSetupPassword, id=ID_SETUP_PSWD)
        self.Bind(wx.EVT_MENU, self.OnSetupProperty, id=ID_SETUP_PROPERTY)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_CLOSE, self.OnExit)

        self.clock = wx.PyTimer(self.OnClockNotify)
        self.clock.Start(1000)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick)

    def OnButtonClick(self, event):
        if event.GetEventObject().GetName() != 'button':
            userId = int(event.GetEventObject().GetName())
            if userId != self.exObjectUserId:
                if userId in self.idList:
                    self.exObjectUserId = userId
                    self.objectUserId = userId
                    self.topPNL.SetObjectUserId(self.objectUserId)
                    self.topPNL.AllRefresh()
                    self.bottomPNL.SetObjectUserId(self.objectUserId)
                    self.bottomPNL.AllRefresh()

    def OnSetupProperty(self, event):
        from PropertyGrid import SetupPropertyDialog
        setupPropertyDLG = SetupPropertyDialog(self)
        setupPropertyDLG.Center(wx.BOTH)
        setupPropertyDLG.ShowModal()
        setupPropertyDLG.Destroy()

    def OnSetupPassword(self, event):
        from ModifyUserPasswordDialog import ModifyUserPasswordDialog
        modifyUserPasswordDLG = ModifyUserPasswordDialog(self, "修改用户密码对话框",
                                                         self.passwordList[self.idList.index(self.myId)])
        modifyUserPasswordDLG.Center(wx.HORIZONTAL)
        if modifyUserPasswordDLG.ShowModal() == wx.ID_OK:
            ourchatDB = MySQL.OurchatDB()
            error = ourchatDB.UpdatePassword(self.myId, modifyUserPasswordDLG.GetValue())
            if error == ID_NO_ERROR:
                wx.MessageBox("修改密码成功，新密码已启用！")
                self.myPassword = modifyUserPasswordDLG.GetValue()
            else:
                wx.MessageBox("密码修改失败！！！")
        modifyUserPasswordDLG.Destroy()

    def OnSetupPersonalInfo(self, event):
        from PersonalPropertyDialog import PersonalPropertyDialog
        setupPersonalInfoDLG = PersonalPropertyDialog(self, self.myId, self.myNickName, myIcon=self.myIcon,
                                                      myHomeTown=self.myHomeTown, size=(400, 600))
        setupPersonalInfoDLG.Centre()
        setupPersonalInfoDLG.ShowModal()
        self.myNickName, self.myHomeTown, self.myIcon, bmp = setupPersonalInfoDLG.GetValue()
        self.topPNL.UpdateMyBmp()
        self.topPNL.AllRefresh()
        if bmp != '':
            self.personalPropertyBTN.SetBitmap(bmp)
        setupPersonalInfoDLG.Destroy()

    def CreateTopPanel(self):
        self.topWIN.Freeze()
        vbox = wx.BoxSizer(wx.VERTICAL)
        from MyHistoryChatPanel import MyHistoryChatPanel
        self.topPNL = MyHistoryChatPanel(self.topWIN, self.myId, self.myNickName,
                                         self.myFriendList, self.myFriendInfoList,
                                         self.checkoutBkgCOLOUR)
        vbox.Add(self.topPNL, 1, wx.EXPAND)
        self.topWIN.SetSizer(vbox)
        self.topWIN.Layout()
        self.topWIN.Thaw()

    def CreateBottomPanel(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        from MyCurrentChatPanel import MyCurrentChatPanel
        self.bottomPNL = MyCurrentChatPanel(self.bottomWIN, self.myId, self.objectUserId)
        vbox.Add(self.bottomPNL, 1, wx.EXPAND)
        self.bottomWIN.SetSizer(vbox)
        self.bottomWIN.Layout()

    def CreateMiddlePanel(self):
        # self.middleWIN.Freeze()
        vbox = wx.BoxSizer(wx.VERTICAL)
        from MyMiddlePanel import MiddlePanel
        self.middlePanel = MiddlePanel(self.middleWIN, -1, size=(100, 100))
        ourchatDB = MySQL.OurchatDB()
        error, data = ourchatDB.GetMyOwnInfo(self.myId)
        if error == ID_NO_ERROR:
            self.myNickName = data[0]
            self.myName = data[1]
            self.myPassword = data[2]
            self.myFriendList = data[3].split(',')
            self.myIcon = data[4]
            self.myHomeTown = data[5]
        else:
            wx.MessageBox("无法打开用户信息数据库，登录失败！")
        self.myFriendInfoList = []
        self.iconThreadList = []
        for friendId in self.myFriendList:
            ourchatDB = MySQL.OurchatDB()
            error, data = ourchatDB.GetFriendInfo(int(friendId))
            if error == ID_NO_ERROR:
                self.myFriendInfoList.append(data)
            else:
                wx.MessageBox("无法打开用户信息数据库，登录失败！")
            thread = self.middlePanel.AddItem(self.myId, friendId, data[1], data[2], data[3], data[4])
            self.iconThreadList.append(thread)
        self.middlePanel.MyRefresh()
        vbox.Add(self.middlePanel, 1, wx.EXPAND)
        self.middleWIN.SetSizer(vbox)
        self.middleWIN.Layout()
        # self.middleWIN.Thaw()

    def CreateLeftPanel(self):
        self.leftWIN.Freeze()
        vbox = wx.BoxSizer(wx.VERTICAL)
        if self.myIcon != '':
            with open(DEFAULT_PATH + '/ls.png', 'wb') as file:
                image = base64.b64decode(self.myIcon)  # 解码
                file.write(image)
            bmp = wx.Bitmap(DEFAULT_PATH + '/ls.png')
        else:
            bmp = wx.Bitmap(USER_PATH + '/%s.png' % self.myId)
        self.personalPropertyBTN = wx.Button(self.leftWIN, -1, size=(60, 60), name='修改个人信息')
        self.personalPropertyBTN.Bind(wx.EVT_BUTTON, self.OnSetupPersonalInfo)
        self.personalPropertyBTN.SetToolTip("修改个人信息")
        self.personalPropertyBTN.SetBitmap(bmp)
        vbox.Add(self.personalPropertyBTN, 0)
        vbox.Add((-1, 100))
        bmp = wx.Bitmap(ICO_PATH + '/13.png')
        btn = wx.Button(self.leftWIN, -1, size=(60, 60))
        btn.SetToolTip("功能待定")
        btn.SetBitmap(bmp)
        vbox.Add(btn, 0)
        vbox.Add((-1, 100), 1)
        bmp = wx.Bitmap(ICO_PATH + '/15.png')
        btn = wx.Button(self.leftWIN, -1, size=(60, 60))
        btn.SetToolTip("功能待定")
        btn.SetBitmap(bmp)
        vbox.Add(btn, 0)
        self.leftWIN.SetSizer(vbox)
        self.leftWIN.Layout()
        self.leftWIN.Thaw()

    def CreateWinStruct(self):
        self.Freeze()
        self.SetMenuBar(self.checkoutMENUBAR)
        self.SetStatusBar(self.statusbar)
        self.Center(wx.BOTH)
        leftWIN = wx.adv.SashLayoutWindow(
            self, -1, wx.DefaultPosition, (200, 30),
            wx.NO_BORDER
        )

        leftWIN.SetDefaultSize((60, -1))
        leftWIN.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        leftWIN.SetAlignment(wx.adv.LAYOUT_LEFT)
        leftWIN.SetBackgroundColour(wx.Colour(230, 230, 230))
        # leftWIN.SetSashVisible(wx.adv.SASH_RIGHT, True)
        # leftWIN.SetExtraBorderSize(0)
        self.leftWIN = leftWIN
        self.winids.append(leftWIN.GetId())

        middleWIN = wx.adv.SashLayoutWindow(
            self, -1, wx.DefaultPosition, (200, 30),
            wx.NO_BORDER
        )

        middleWIN.SetDefaultSize((250, -1))
        middleWIN.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        middleWIN.SetAlignment(wx.adv.LAYOUT_LEFT)
        middleWIN.SetBackgroundColour(wx.Colour(235, 235, 235))
        middleWIN.SetSashVisible(wx.adv.SASH_RIGHT, True)

        self.middleWIN = middleWIN
        self.winids.append(middleWIN.GetId())

        bottomWIN = wx.adv.SashLayoutWindow(
            self, -1, wx.DefaultPosition, (200, 30),
            wx.NO_BORDER
        )

        bottomWIN.SetDefaultSize((300, 200))
        bottomWIN.SetOrientation(wx.adv.LAYOUT_HORIZONTAL)
        bottomWIN.SetAlignment(wx.adv.LAYOUT_BOTTOM)
        bottomWIN.SetSashVisible(wx.adv.SASH_TOP, True)

        self.bottomWIN = bottomWIN
        self.winids.append(bottomWIN.GetId())

        self.topWIN = wx.Panel(self, -1)
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.topWIN)
        self.Thaw()
        self.Bind(
            wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnSashDrag,
            id=min(self.winids), id2=max(self.winids)
        )
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnCheckin(self, event):
        self.GetUserInfo()
        if self.exId not in self.idList:
            self.exId = self.idList[0]
        self.userName = self.userList[self.idList.index(self.exId)]
        checkinDLG = CheckinDialog(self, -1, '用户登录', self.userList)
        checkinDLG.Center()
        if checkinDLG.ShowModal() == wx.ID_OK:
            checkinDLG.Destroy()
            userName, password = checkinDLG.GetValue()
            if self.passwordList[self.userList.index(userName)] != password:
                wx.MessageBox("密码错误，请重新登录！", "信息提示")
            else:
                self.cpuId = WMI().Win32_Processor()[0].ProcessorId.strip()
                self.checkinState = True
                self.myId = self.idList[self.userList.index(userName)]
                ourchatDB = MySQL.OurchatDB()
                ourchatDB.UpdateCPUId(self.myId, self.cpuId)
                self.kickoutThread = KickOutThread(self, self.myId, self.cpuId)
                self.Bind(Evt_KICKOUT, self.OnKickout)
                self.kickoutThread.Start(self.myId, self.cpuId)
                self.kickoutTimer = wx.PyTimer(self.OnKickoutTimer)
                self.kickoutTimer.Start(100)
                if self.myId != self.exId:
                    self.exId = self.myId
                    self.mainConfig.UpdateValue(self.myId, self.exIdTIP, self.exUserList, self.exUserListTIP)
                self.myName = userName
                self.myIcon = self.iconList[self.userList.index(userName)]
                self.statusbar.SetStatusText("%s 已登录" % self.userName, 2)
                self.CreateWinStruct()
                self.CreateTopPanel()
                self.CreateLeftPanel()
                self.CreateMiddlePanel()
                self.CreateBottomPanel()
                self.SetMenuBar(self.checkinMENUBAR)

    def OnKickout(self, event):
        self.CheckOut()
        wx.MessageBox("有新用户在%s设备上以此账号登录，您被强行退出登录状态!" % event.newCPUId)

    def OnKickoutTimer(self):
        self.kickoutThread.Start(self.myId, self.cpuId)

    def OnCheckout(self, event):
        self.CheckOut()

    def CheckOut(self):
        self.checkinState = False
        self.exObjectUserId = 0
        self.clock.Stop()
        self.Unbind(wx.EVT_SIZE)
        for item in self.middlePanel.itemList:
            item.friendInfoUpdater.Stop()
        self.topPNL.messageUpdater.Stop()
        for iconThread in self.iconThreadList:
            iconThread.Stop()
        self.topPNL.readNewMessageTHREAD.Stop()
        self.DestroyChildren()  # 如果不关闭线程就DestroyChildren，会导致线程触发的事件无人处理，从而造成（1次）报错错误
        self.SetMenuBar(self.checkoutMENUBAR)
        self.CreateMyStatusBar()
        self.SetStatusBar(self.statusbar)
        self.clock.Start(100)
        del self.kickoutTimer
        del self.kickoutThread

    def InitParameter(self):
        self.checkinState = False
        self.winids = []  # SashWindow结构要用的各个窗口分区的ID列表
        self.myId = 0  # 登录系统的用户ID
        self.myNickName = ''  # 登录系统用户的昵称
        self.myName = ''  # 登录系统用户的实际姓名
        self.myPassword = ''  # 登录系统用户的密码
        self.myIcon = ''  # 登录系统用户的头像
        self.myHomeTown = ''  # 登录系统用户的所在位置
        self.objectUserId = 0  # 当前聊天对象的ID
        self.threads = []  # 线程列表,在checkin后需要时要append、checkout时先Stop再清空、程序close时Stop
        self.messageList = []  # 消息列表
        self.checkoutBkgCOLOUR = wx.Colour(240, 240, 240)  # 登出状态下的背景颜色
        self.checkinBkgCOLOUR = wx.Colour(255, 255, 255)  # 登录状态下的背景颜色
        self.myFriendList = []  # 好友列表：[friend1Id,friend2Id,.....]按在user表单中的Index升序排列
        self.myFriendInfoList = []  # 好友信息列表：[[friendId,friendNickName,friendName,friendIcon,friend]]
        self.exObjectUserId = 0

    def AdjustSize(self, size):
        if wx.GetDisplaySize().width < size.Width:
            size.Width = wx.GetDisplaySize().width
        if wx.GetDisplaySize().height < size.Height + 100:
            size.Height = wx.GetDisplaySize().Height - 100
        self.SetSize(size)

    def CreateMyMenuBar(self):
        self.checkinMENUBAR = wx.MenuBar()
        self.checkMENU = wx.Menu()
        self.checkMENU.Append(ID_SETUP_PSWD, "修改用户密码")
        self.checkMENU.Append(ID_CHECKOUT, "登出")
        self.checkMENU.AppendSeparator()
        self.checkMENU.Append(wx.ID_EXIT, "退出")
        self.setupMENU = wx.Menu()
        self.setupMENU.Append(ID_SETUP_PROPERTY, "系统参数设置")
        self.helpMENU = wx.Menu()
        self.helpMENU.Append(ID_HELP, "关于")
        self.checkinMENUBAR.Append(self.checkMENU, "&F. 文件")
        self.checkinMENUBAR.Append(self.setupMENU, "&S. 系统设置")
        self.checkinMENUBAR.Append(self.helpMENU, "&H. 帮助")

        self.checkoutMENUBAR = wx.MenuBar()
        self.checkMENU = wx.Menu()
        self.checkMENU.Append(ID_CHECKIN, "登录")
        self.checkMENU.AppendSeparator()
        self.checkMENU.Append(wx.ID_EXIT, "退出")
        self.setupMENU = wx.Menu()
        self.setupMENU.Append(ID_SETUP_PROPERTY, "系统参数设置")
        self.helpMENU = wx.Menu()
        self.helpMENU.Append(ID_HELP, "关于")
        self.checkoutMENUBAR.Append(self.checkMENU, "&F. 文件")
        self.checkoutMENUBAR.Append(self.setupMENU, "&S. 系统设置")
        self.checkoutMENUBAR.Append(self.helpMENU, "&H. 帮助")

    def CreateMyStatusBar(self):
        self.statusbar = wx.StatusBar(self, -1, style=wx.STB_SIZEGRIP)
        self.statusbar.SetFieldsCount(4)
        self.statusbar.SetStatusWidths([100, -2, 90, 140])
        self.statusbar.SetStatusText("ready", 0)
        self.statusbar.SetStatusText("程序正在运行。。。", 1)
        self.statusbar.SetStatusText("未登录", 2)
        self.SetStatusBar(self.statusbar)

    def OnExit(self, event):
        if self.checkinState:
            busy = wx.BusyInfo("One moment please, waiting for threads to die...")
            wx.Yield()
            for item in self.middlePanel.itemList:
                item.friendInfoUpdater.Stop()
            self.topPNL.messageUpdater.Stop()
            for iconThread in self.iconThreadList:
                iconThread.Stop()
            self.topPNL.readNewMessageTHREAD.Stop()
        self.clock.Stop()
        self.Unbind(wx.EVT_SIZE)
        self.Destroy()

    def OnAbout(self, event):
        # First we create and fill the info object
        info = wx.adv.AboutDialogInfo()
        info.Name = "我们自己的线上聊天小程序 "
        info.Version = " %s" % VERSION
        info.Copyright = "(c) 2020-2025 天津大学精密仪器与光电子工程学院"
        info.Description = wordwrap(
            "      一款通过云端数据库实现的在线聊天小程序。"
            "其开发目的主要是帮助在校      \r\n大学生学习Python语言编程技术。"
            "本程序的代码全部使用Python语言编写，\r\n并在 Python3.7 环境下调试通过。"

            "\n\n本程序涉及："
            "\r\n  1. 页面布局；菜单、工具条、状态栏的创建和使用；"
            "\r\n  2. 消息循环建立、事件绑定、菜单、按钮等Windows控件的消息响应；"
            "\r\n  3. MySQL数据库连接、创建、写入、查询、更新等操作的编程方法；"
            "\r\n  4. 多线程、消息派遣、异常处理等编程技术",
            800, wx.ClientDC(self))
        info.WebSite = ("http://en.wikipedia.org/wiki/Hello_world", "Hello World home page")
        info.Developers = ["指导教师：李一博\r\n研究生：覃文静",
                           "滕晨琳", '吴姊涵',
                           "窦迪航"]

        info.License = wordwrap(licenseText, 500, wx.ClientDC(self))

        # Then we call wx.AboutBox giving it that info object
        wx.adv.AboutBox(info)

    def OnSashDrag(self, event):
        if event.GetDragStatus() == wx.adv.SASH_STATUS_OUT_OF_RANGE:
            return

        eobj = event.GetEventObject()

        if eobj is self.leftWIN:
            self.leftWIN.SetDefaultSize((event.GetDragRect().width, 1000))
        elif eobj is self.middleWIN:
            self.middleWIN.SetDefaultSize((event.GetDragRect().width, 1000))
        elif eobj is self.bottomWIN:
            self.bottomWIN.SetDefaultSize((1000, event.GetDragRect().height))

        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.topWIN)
        self.topWIN.Refresh()

    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.topWIN)
        self.leftWIN.Layout()
        self.middleWIN.Layout()
        self.bottomWIN.Layout()

    def OnClockNotify(self):
        t = time.localtime(time.time())
        st = time.strftime("%Y年%m月%d日 %H:%M:%S", t)
        self.statusbar.SetStatusText(st, 3)
