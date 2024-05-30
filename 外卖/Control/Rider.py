import sql
import random
# 骑手属性集
attributeList_rider = [
    ("RID","工号"),
    ("Rname","姓名"),
    ("Rphone","电话")
]

class RiderManager(object):
    """骑手管理类, 单例"""

    def __init__(self):
        # 用于存储所有骑手对象
        self.RList = []
        # 工号 -> 骑手对象
        self.rider_RID = {}

        self.load()

        self.emptyRider = Rider()

    def add(self, rider):
        rider.SID = str(random.randint(0,999)).rjust(3, '0')
        while(sql.check_user(rider.SID, rider)[0] == False):
            rider.SID = str(random.randint(0,999)).rjust(3, '0')
        self.RList.append(rider)
        self.rider_RID[rider.RID] = rider
        return sql.rider_add(rider)

    def delete(self, rider):
        self.rider_RID.pop(rider.RID)
        self.RList.remove(rider)
        sql.rider_delete(rider)
        return True

    def multiSearch(self, keyList):
        # print(keyList)
        searchBy = []
        keyText = []
        #print(keyList)
        for searchby, keytext in keyList:
            if keytext:
                searchBy.append(searchby)
                keyText.append(keytext)
        msg = sql.rider_multiselect(searchBy, keyText)
        #print(searchBy)
        #print(keyText)
        result = self.torider(msg)
        return result

    def search(self, searchBy, keyList):
        #print(searchBy)
        result = []
        if not keyList:
            result = self.load()
            return result
        else:
            msg = sql.rider_select(searchBy, keyList)
            result = result + self.torider(msg)
            return result

    def torider(self,msg):
        result = []
        for i in range(len(msg)):
            # 创建每一个数据的rider对象
            m = msg[i]
            # print(s)
            rider = Rider()
            rider.RID = m[0]
            rider.Rname = m[1]
            rider.Rphone = m[2]
            result.append(rider)
        return result

    def load(self):
        RList = []
        rider_RID = {}
        try:
            msg = sql.Load("m_table")
            result = self.torider(msg)
            for rider in result:
                RList.append(rider)
                rider_RID[rider.RID] = rider
            result = True
        except:
            result = False
        finally:
            self.RList = RList
            self.rider_RID = rider_RID

        #print(self.MMID)
        #print(self.MList)
        return RList
    
class Rider(object):
    """骑手类, 用于存储骑手基本信息"""
    def __init__(self, RID="", Rname="", Rphone=""):
        self.RID = RID
        self.Rname = Rname
        self.Rphone = Rphone

    def copy(self):
        rider = Rider()
        self.copyTo(rider)
        return rider

    def copyTo(self, rider):
        rider.RID = self.RID
        rider.Rname = self.Rname
        rider.Rphone = self.Rphone

    def checkInfo(self,new=False):
        '''检查自身信息是否完整合法'''
        # 空值检测
        for attr, text in attributeList_rider:
            if not getattr(self, attr):
                return (False, "%s不能为空" % text)
        # 重复性检测
        check = sql.check_rider(self.RID, new)
        if check[0] ==0:
            return check

        return (True, "")
