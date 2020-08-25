import wx
import MySQL


class ModifyUserPasswordDialog(wx.Dialog):
    def __init__(self, parent, title, oldPassword, size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE, name='Checkin Dialog'):
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, -1, title, pos, size, style, name)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer()
        self.oldPassword = oldPassword
        self.oldPasswordTXT = wx.TextCtrl(self, -1, value = '', size=(150, 25))
        hbox.Add((10, -1))
        hbox.Add(wx.StaticText(self, label="请输入原密码："), 0, wx.TOP, 5)
        hbox.Add(self.oldPasswordTXT, 1, wx.LEFT, 10)
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 5)
        hbox = wx.BoxSizer()
        self.newPassword1TXT = wx.TextCtrl(self, -1, size=(150, 25), style=wx.TE_PASSWORD)
        hbox.Add((10, -1))
        hbox.Add(wx.StaticText(self, label="请输入新密码："), 0, wx.TOP, 5)
        hbox.Add(self.newPassword1TXT, 1, wx.LEFT, 10)
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 5)
        hbox = wx.BoxSizer()
        self.newPassword2TXT = wx.TextCtrl(self, -1, size=(150, 25), style=wx.TE_PASSWORD)
        hbox.Add((10, -1))
        hbox.Add(wx.StaticText(self, label="请再输入一遍："), 0, wx.TOP, 5)
        hbox.Add(self.newPassword2TXT, 1, wx.LEFT, 10)
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
        self.oldPasswordTXT.SetFocus()
    def OnOk(self, event):
        if(self.oldPasswordTXT.GetValue() == self.oldPassword):
            if((self.newPassword1TXT.GetValue() != '') and (self.newPassword1TXT.GetValue() == self.newPassword2TXT.GetValue())):
                self.oldPassword = self.newPassword1TXT.GetValue()
                event.Skip()
    def GetValue(self):
        return self.newPassword1TXT.GetValue()