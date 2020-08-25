import math
import wx.lib.scrolledpanel as scrolled
from MyThreads import *


class MyHistoryChatPanel(wx.Panel):
    def __init__(self, parent, myId, myNickName, myFriendList, myFriendInfoList, bkColour):
        wx.Panel.__init__(self, parent, -1, name="HistoryChatPanel")
        self.CTRL = []
        self.myId = myId
        self.objectUserId = 0
        self.myBMP = wx.Bitmap(USER_PATH + '/%s.png' % str(self.myId))
        self.myNickName = myNickName
        self.myFriendList = myFriendList
        self.myFriendInfoList = myFriendInfoList
        self.lastMessageRecordIndex = 0
        self.messageList = []
        self.lastIcon = None
        self.lastMessageTime = None
        self.objectUserBMP = None
        self.myIdBMP = None
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer()
        font = wx.Font(16, wx.DECORATIVE, wx.FONTSTYLE_NORMAL, wx.NORMAL)
        self.nameLABEL = wx.StaticText(self, -1, label='', size=(150, -1))
        self.nameLABEL.SetFont(font)
        self.historyChatPropertyBTN = wx.Button(self, -1, label="设置", size=(60, -1))
        self.historyChatPropertyBTN.Enable(False)
        self.historyChatPropertyBTN.Bind(wx.EVT_BUTTON, self.OnHistoryChatPropertySetup)
        hbox = wx.BoxSizer()
        hbox.Add((10, -1))
        hbox.Add(self.nameLABEL, 0, flag=wx.TOP, border=10)
        hbox.Add((100, -1), 1)
        hbox.Add(self.historyChatPropertyBTN, 0, flag=wx.EXPAND | wx.ALL, border=8)
        vbox.Add(hbox, 0, wx.EXPAND)
        self.messagePNL = scrolled.ScrolledPanel(self, -1)
        self.messageBox = wx.BoxSizer(wx.VERTICAL)
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        vbox.Add(line, 0, wx.GROW, 5)
        self.messagePNL.SetSizer(self.messageBox)
        # self.messagePNL.SetAutoLayout(1)
        # self.messagePNL.SetupScrolling()
        self.messagePNL.SetScrollPos(wx.VERTICAL, -1)

        vbox.Add(self.messagePNL, 1, wx.EXPAND)
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        vbox.Add(line, 0, wx.GROW | wx.TOP | wx.BOTTOM, 2)
        self.SetSizer(vbox)
        self.Layout()
        self.messageUpdater = wx.PyTimer(self.StartUpdateMessage)
        self.messageUpdater.Start(100)
        self.readNewMessageTHREAD = ReadNewMessagesThread(self)
        self.Bind(EVT_UPDATE_NEWMESSAGES, self.OnUpdateNewMessages)

    def OnHistoryChatPropertySetup(self, event):
        from wx.lib import stattext
        self.sampleText = stattext.GenStaticText(self, -1, "Sample Text")
        self.curFont = self.sampleText.GetFont()
        self.curClr = wx.BLACK
        data = wx.FontData()
        data.EnableEffects(True)
        data.SetColour(self.curClr)  # set colour
        data.SetInitialFont(self.curFont)
        dlg = wx.FontDialog(self, data)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            self.curFont = data.GetChosenFont()
            self.curClr = data.GetColour()
            for label in self.CTRL:
                label.SetFont(self.curFont)
                label.SetForegroundColour(self.curClr)
            self.messagePNL.Layout()

    def OnUpdateNewMessages(self, event):
        if event.newMessages:
            for message in event.newMessages:
                self.messageList.append(message)
                hbox = wx.BoxSizer()
                if self.objectUserId != 0:
                    if message[1] == self.objectUserId:
                        hbox.Add((10, -1))
                        icon = wx.StaticBitmap(self.messagePNL, -1, self.objectUserBMP, size=(48, 48))
                        hbox.Add(icon, 0)
                        hbox.Add((10, -1))
                        length = len(message[3])
                        if length < 15:
                            size = (length * 12 + 20, 20)
                        else:
                            size = (200, math.ceil(length / 15.) * 20)
                        panel = wx.Panel(self.messagePNL, size=size)
                        panel.SetBackgroundColour(wx.Colour(255, 255, 255))
                        vvbox = wx.BoxSizer(wx.VERTICAL)
                        label = wx.StaticText(panel, -1, label=message[3], size=(100, 100))
                        vvbox.Add(label, 1, wx.EXPAND | wx.ALL, 2)
                        panel.SetSizer(vvbox)
                        hbox.Add(panel, 0)
                        self.messageBox.Add(hbox, 0)
                        self.messageBox.Add((-1, 10))
                    else:
                        hbox.Add((10, -1), 1)
                        length = len(message[3])
                        if length < 15:
                            size = (length * 12 + 20, 20)
                        else:
                            size = (200, math.ceil(length / 15.) * 20)
                        panel = wx.Panel(self.messagePNL, size=size)
                        panel.SetBackgroundColour(wx.Colour(0, 255, 0))
                        vvbox = wx.BoxSizer(wx.VERTICAL)
                        label = wx.StaticText(panel, -1, label=message[3], size=(100, 100))
                        vvbox.Add(label, 1, wx.EXPAND | wx.ALL, 2)
                        panel.SetSizer(vvbox)
                        hbox.Add(panel, 0)
                        hbox.Add((10, -1), 0)
                        icon = wx.StaticBitmap(self.messagePNL, -1, self.myBMP, size=(48, 48))
                        hbox.Add(icon, 0)
                        hbox.Add((10, -1), 0)
                        self.messageBox.Add(hbox, 0, wx.EXPAND)
                        self.messageBox.Add((-1, 10))
                    self.CTRL.append(label)
                    self.lastIcon = icon
            self.messagePNL.SetSizer(self.messageBox)
            self.messagePNL.SetAutoLayout(1)
            self.messagePNL.SetupScrolling(scrollToTop=False)
            self.lastIcon.SetFocus()
            self.lastMessageRecordIndex = self.messageList[-1][0]

    def StartUpdateMessage(self):
        if self.objectUserId != 0:
            self.readNewMessageTHREAD.Start(self.lastMessageRecordIndex, self.myId, self.objectUserId)

    def GetAllMessages(self, userId, objectUserId):
        self.messageList = []
        ourchatDB = MySQL.OurchatDB()
        error, data = ourchatDB.ReadMessages(userId, objectUserId)
        self.lastMessageRecordIndex = 0
        if error == ID_NO_ERROR:
            if len(data) != 0:
                self.messageList = []
                for record in data:
                    self.messageList.append(record)
                self.lastMessageRecordIndex = self.messageList[-1][0]
                ourchatDB = MySQL.OurchatDB()
                error = ourchatDB.UpdateMessagesHaveRead(userId, objectUserId)

    def UpdateMyBmp(self):
        self.myBMP = wx.Bitmap(USER_PATH + '/%s.png' % str(self.myId))

    def SetObjectUserId(self, objectUserId):
        self.objectUserId = objectUserId
        self.objectUserBMP = wx.Bitmap(USER_PATH + '/%s.png' % str(self.objectUserId))

    def AllRefresh(self):
        icon = None
        if self.objectUserId != 0:
            self.CTRL = []
            self.messagePNL.Freeze()
            self.objectUserBMP = wx.Bitmap(USER_PATH + '%s.png' % str(self.objectUserId))
            self.myIdBMP = wx.Bitmap(USER_PATH + '%s.png' % str(self.myId))
            self.GetAllMessages(self.myId, self.objectUserId)
            self.historyChatPropertyBTN.Enable(True)
            self.messagePNL.DestroyChildren()
            self.messageBox = wx.BoxSizer(wx.VERTICAL)
            self.messageBox.Add((-1, 20))
            if self.messageList:
                self.lastMessageTime = self.messageList[0][2]

                hbox = wx.BoxSizer()
                hbox.Add((10, -1), 1)
                hbox.Add(wx.StaticText(self.messagePNL, -1, label=str(self.lastMessageTime)))
                hbox.Add((10, -1), 1)
                self.messageBox.Add(hbox, 0, wx.EXPAND)
                self.messageBox.Add((-1, 10))
                for message in self.messageList:
                    mesageTime = message[2]
                    if (message[2] - self.lastMessageTime).seconds > 1200:
                        self.lastMessageTime = message[2]
                        hbox = wx.BoxSizer()
                        hbox.Add((10, -1), 1)
                        hbox.Add(wx.StaticText(self.messagePNL, -1, label=str(self.lastMessageTime)))
                        hbox.Add((10, -1), 1)
                        self.messageBox.Add(hbox, 0, wx.EXPAND)
                        self.messageBox.Add((-1, 10))
                    hbox = wx.BoxSizer()
                    if message[1] == self.objectUserId:
                        hbox.Add((10, -1))
                        icon = wx.StaticBitmap(self.messagePNL, -1, self.objectUserBMP, size=(48, 48))
                        hbox.Add(icon, 0)
                        hbox.Add((10, -1))
                        length = len(message[3])
                        if length < 15:
                            size = (length * 12 + 20, 20)
                        else:
                            size = (200, math.ceil(length / 15.) * 20)
                        panel = wx.Panel(self.messagePNL, size=size)
                        panel.SetBackgroundColour(wx.Colour(255, 255, 255))
                        vvbox = wx.BoxSizer(wx.VERTICAL)
                        text = wx.StaticText(panel, -1, label=message[3], size=(100, 100))
                        vvbox.Add(text, 1, wx.EXPAND | wx.ALL, 2)
                        panel.SetSizer(vvbox)
                        hbox.Add(panel, 0)
                        self.messageBox.Add(hbox, 0)
                        self.messageBox.Add((-1, 10))
                    else:
                        hbox.Add((10, -1), 1)
                        length = len(message[3])
                        if length < 15:
                            size = (length * 12 + 20, 20)
                        else:
                            size = (200, math.ceil(length / 15.) * 20)
                        panel = wx.Panel(self.messagePNL, size=size)
                        panel.SetBackgroundColour(wx.Colour(0, 255, 0))
                        vvbox = wx.BoxSizer(wx.VERTICAL)
                        text = wx.StaticText(panel, -1, label=message[3], size=(100, 100))
                        vvbox.Add(text, 1, wx.EXPAND | wx.ALL, 2)
                        panel.SetSizer(vvbox)
                        hbox.Add(panel, 0)
                        hbox.Add((10, -1), 0)
                        icon = wx.StaticBitmap(self.messagePNL, -1, self.myBMP, size=(48, 48))
                        hbox.Add(icon, 0)
                        hbox.Add((10, -1), 0)
                        self.messageBox.Add(hbox, 0, wx.EXPAND)
                        self.messageBox.Add((-1, 10))
                    self.CTRL.append(text)
                self.lastIcon = icon
            self.messagePNL.SetSizer(self.messageBox)
            self.messagePNL.SetAutoLayout(1)
            self.messagePNL.SetupScrolling(scrollToTop=False)
            self.lastIcon.SetFocus()
            self.messagePNL.Thaw()
