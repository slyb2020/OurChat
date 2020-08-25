import wx
import MySQL


class CheckinDialog(wx.Dialog):
    def __init__(self, parent, id, title, userList = [],size = wx.DefaultSize, pos = wx.DefaultPosition,
                 style = wx.DEFAULT_DIALOG_STYLE, name = 'Checkin Dialog'):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, id, title, pos, size, style, name)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer()
        self.userList = userList
        self.userNameCOMBO = wx.ComboBox(self, -1, value=parent.userName, choices=self.userList, size=(150, 25),
                                    style=wx.CB_READONLY)
        hbox.Add((10, -1))
        hbox.Add(wx.StaticText(self, label="请选择用户名："), 0, wx.TOP, 5)
        hbox.Add(self.userNameCOMBO, 1, wx.LEFT, 10)
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 5)
        hbox = wx.BoxSizer()
        self.passwordTXT = wx.TextCtrl(self, -1, size=(150, 25), style=wx.TE_PASSWORD)
        hbox.Add((10, -1))
        hbox.Add(wx.StaticText(self, label="请您输入密码："), 0, wx.TOP, 5)
        hbox.Add(self.passwordTXT, 1, wx.LEFT, 10)
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 5)
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        vbox.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)
        btnsizer = wx.StdDialogButtonSizer()
        okBTN = wx.Button(self, wx.ID_OK, '确定')
        okBTN.SetDefault()
        btnsizer.AddButton(okBTN)
        cancelBTN = wx.Button(self, wx.ID_CANCEL, '取消')
        btnsizer.AddButton(cancelBTN)
        btnsizer.Realize()
        vbox.Add(btnsizer, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        self.SetSizer(vbox)
        vbox.Fit(self)
        okBTN.Bind(wx.EVT_BUTTON, self.OnOk)
        self.userNameCOMBO.Bind(wx.EVT_COMBOBOX, self.OnNameChange)
        self.passwordTXT.SetFocus()
    def OnNameChange(self,event):
        self.passwordTXT.SetFocus()
    def OnOk(self, event):
        if(self.passwordTXT.GetValue() != ''):
            event.Skip()
    def GetValue(self):
        return self.userNameCOMBO.GetValue(), self.passwordTXT.GetValue()