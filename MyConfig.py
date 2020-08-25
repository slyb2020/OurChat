import os
from ID_DEFINE import DEFAULT_PATH

class MyConfig:
    def __init__(self, keyword, filename = DEFAULT_PATH+'setup.cfg'):
        self.configFileName = filename
        self.file = None

    def Open(self):
        isExist = os.path.isfile(self.configFileName)
        self.file = open(self.configFileName, mode = "a+")
        return isExist

    def Close(self):
        self.file.close()

    def Update(self, keyword, value):
        delrow = -1
        self.Open()
        self.file.seek(0)
        contents = self.file.readlines()
        for line in contents:
            if(line.find(keyword) != -1):
                delrow=contents.index(line)
                break
        if(delrow != -1):
            contents.pop(delrow)
        self.Close()
        self.file = open(self.configFileName,'w')
        for line in contents:
            self.file.write(line)
        self.Close()
        self.Append(keyword, value)

    def Get(self, keyword):
        self.Open()
        self.file.seek(0)
        keepgoing = -1
        while keepgoing == -1:
            contents = self.file.readline()
            if(contents != ''):
                keepgoing = contents.find(keyword)
            else:
                keepgoing = 0
                contents = ''
        self.Close()
        return contents
    def Append(self, keyword, value):
        self.Open()
        self.file.write(keyword+'='+'{'+value+'}\n')
        self.Close()
class MainConfig(MyConfig):
    def __init__(self, filename = DEFAULT_PATH+'setup.cfg'):
        self.keyword = "MyInfo"
        MyConfig.__init__(self, self.keyword, filename)

    def GetValue(self):
        success = False
        myId = ''
        myIdTIP = ''
        exUserList = []
        exUserListTIP = ''
        data = self.Get(self.keyword)
        if(data != ''):
            success = True
            data = data[1:].split(';')
            myId = int(data[0].split(':')[1].split('`')[0])
            myIdTIP = data[0].split(':')[1].split('`')[1]
            ls = data[1].split(':')[1].split('`')[0].split(',')
            exUserList = []
            for i in ls:
                exUserList.append(int(i))
            exUserListTIP = data[1].split(':')[1].split('`')[1]
        return success, myId, myIdTIP, exUserList, exUserListTIP
    def UpdateValue(self,myId, myIdTIP, exUserList, exUserListTIP):
        self.Update(self.keyword, "我的ID:%d`%s`; 曾经用户列表:%s`%s`"%(myId, myIdTIP, str(exUserList)[1:-1], exUserListTIP))

class DataBaseConfig(MyConfig):
    def __init__(self, filename = DEFAULT_PATH+'/setup.cfg'):
        self.keyword = "OurChatDB"
        MyConfig.__init__(self, self.keyword, filename)
    def GetValue(self):
        isSuccess = False
        witchDB = 0
        testCloud = ['121.196.217.197','jingyi','jingyi123','test','utf8']
        formalCloud = ['121.196.217.197','jingyi','jingyi123','formal','utf8']
        testLocal = ['127.0.0.1','jingyi','jingyi123','test','utf8']
        formalLocal = ['127.0.0.1','jingyi','jingyi123','formal','utf8']
        data = self.Get(self.keyword)
        if(data != ''):
            isSuccess = True
            data = data[1:].split(';')
            witchDB = int(data[0].split(':')[1].split('`')[0])
            testcloud = data[1].split(':')[1].split('`')[0].split(',')
            foralCloud = data[2].split(':')[1].split('`')[0].split(',')
            testLocal = data[3].split(':')[1].split('`')[0].split(',')
            formalLocal = data[4].split(':')[1].split('`')[0].split(',')
        return isSuccess, witchDB, testCloud, formalCloud, testLocal, formalLocal
    def UpdateValue(self,witchDB, testCloud, formalCloud, testLocal, formalLocal):
        self.Update(self.keyword, "选择的数据库:%d``; 云端测试:%s,%s,%s,%s``; 云端正式:%s,%s,%s,%s``; "
                                  "本地测试:%s,%s,%s,%s``; 本地正式:%s,%s,%s,%s``"
                    %(witchDB,testCloud[0],testCloud[1],testCloud[2],testCloud[3],
                      formalCloud[0],formalCloud[1],formalCloud[2],formalCloud[3],
                      testLocal[0],testLocal[1],testLocal[2],testLocal[3],
                      formalLocal[0],formalLocal[1],formalLocal[2],formalLocal[3]))