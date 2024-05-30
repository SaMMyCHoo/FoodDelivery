import sql
import random
# 用户属性集
attributeList_user = [
    ("UID","用户号"),
    ("Uname","用户名"),
    ("Uaddr","地址"),
    ("Uphone","电话号")
]
class UserManager(object):
    """用户管理类, 单例"""

    def __init__(self):
        # 用于存储所有用户对象
        self.userList = []
        # 用户号 -> 用户对象
        self.userUID = {}

        self.load()

        self.emptyUser = User()

    def add(self, user):
        user.UID = str(random.randint(0,999)).rjust(3, '0')
        while(sql.check_user(user.UID, user)[0] == False):
            user.UID = str(random.randint(0,999)).rjust(3, '0')
        self.userList.append(user)
        self.userUID[user.UID] = user
        return sql.user_add(user)

    def delete(self, user):
        self.userUID.pop(user.UID)
        self.userList.remove(user)
        return sql.user_delete(user)

    def multiSearch(self, keyList):
        #print(keyList)
        searchBy = []
        keyText = []
        # print(keyList)
        for searchby, keytext in keyList:
            if keytext:
                searchBy.append(searchby)
                keyText.append(keytext)
        msg = sql.user_multiselect(searchBy,keyText)
        print(searchBy)
        print(keyText)
        result = self.touser(msg)
        return result

    def search(self, searchBy, keyList):
        #print(searchBy)
        result = []
        if not keyList:
            result = self.load()
            return result
        else:
            msg = sql.user_select(searchBy,keyList)
            result = result + self.touser(msg)
            #print(result)
            return result

    def touser(self,msg):
        result = []
        for i in range(len(msg)):
            # 创建每一个数据的user对象
            s = msg[i]
            # print(s)
            user = User()
            user.UID = s[0]
            user.Uname = s[1]
            user.Uaddr = s[2]
            user.Uphone = s[3]
            result.append(user)
        return result

    def load(self):
        userList = []
        userUID = {}
        try:
            msg = sql.Load("x_table")
            result = self.touser(msg)
            for user in result:
                #print(user)
                #创建每一个数据的user对象
                userList.append(user)
                userUID[user.UID] = user
            result = True
        except:
            result = False
        finally:
            self.userList = userList
            self.userUID = userUID

        #print(self.userUID)
        #print(self.userList)
        return userList

class User(object):
    """用户类, 用于存储用户基本信息"""
    def __init__(self, UID="", Uname="", Uaddr="", Uphone=""):
        self.UID = UID
        self.Uname = Uname
        self.Uaddress = Uaddr
        self.Uphone = Uphone

    # def getSex(self):
    #     return ["", "男", "女"][self.Ssex]

    def copy(self):
        user = User()
        self.copyTo(user)
        return user

    def copyTo(self, user):
        user.UID = self.UID
        user.Uname = self.Uname
        user.Uaddr = self.Uaddr
        user.Uphone = self.Uphone

    def checkInfo(self,new=False):
        '''检查自身信息是否完整合法'''
        # 空值检测
        for attr, text in attributeList_user:
            if not getattr(self, attr):
                return (False, "%s不能为空" % text)
        # 重复性检测
        check = sql.check_user(self.UID, new)
        if check[0] == 0:
            return check

        return (True, "")