import wx
import MySQL


class MyCurrentChatPanel(wx.Panel):
    def __init__(self, parent, myId, objectUserId, bkColour=wx.Colour(240, 240, 240)):
        wx.Panel.__init__(self, parent, -1, name="CurrentChatPanel")
        self.myId = myId
        self.objectUserId = 0
        self.Freeze()
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer()
        self.toolBTNS = []
        for i in range(5):
            btn = wx.Button(self, -1, label='', size=(20, 20))
            hbox.Add(btn, 0, wx.ALL, border=1)
            btn.Enable(False)
            self.toolBTNS.append(btn)
        vbox.Add(hbox, 0, wx.EXPAND)
        self.currentMessageTXT = wx.TextCtrl(self, -1, size=(-1, 100), style=wx.TE_MULTILINE)
        vbox.Add(self.currentMessageTXT, 1, wx.EXPAND)
        hbox = wx.BoxSizer()
        hbox.Add((300, -1), proportion=1)
        self.sendBTN = wx.Button(self, label="发送", size=(80, 25))
        hbox.Add(self.sendBTN, 0, wx.ALL, border=5)
        vbox.Add(hbox, 0, wx.EXPAND)
        self.currentMessageTXT.Enable(False)
        self.sendBTN.Enable(False)
        self.SetSizer(vbox)
        self.Layout()
        self.Thaw()
        self.currentMessageTXT.Bind(wx.EVT_TEXT, self.OnMessageInput)
        self.sendBTN.Bind(wx.EVT_BUTTON, self.Send)

    def OnMessageInput(self, event):
        if self.currentMessageTXT.GetValue() == '':
            self.sendBTN.Enable(False)
        else:
            self.sendBTN.Enable(True)

    def Send(self, event):
        ourchatDB = MySQL.OurchatDB()
        ourchatDB.SaveMessage(self.myId, self.currentMessageTXT.GetValue(), self.objectUserId)
        self.currentMessageTXT.ChangeValue('')
        self.currentMessageTXT.SetFocus()
        self.sendBTN.Enable(False)

    def SetObjectUserId(self, objectUserId):
        self.objectUserId = objectUserId

    def AllRefresh(self):
        self.currentMessageTXT.ChangeValue("")
        if self.objectUserId != 0:
            self.currentMessageTXT.SetBackgroundColour(wx.Colour(255, 255, 255))
            self.currentMessageTXT.Enable(True)
            for btn in self.toolBTNS:
                btn.Enable(True)
            self.currentMessageTXT.SetFocus()
