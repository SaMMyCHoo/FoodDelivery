import sql
import random
# 商家属性集
attributeList_seller = [
    ("SID","商家号"),
    ("Sname","商家名"),
    ("Saddr","商家地址"),
    ("Sphone","商家电话")
]

class SellerManager(object):
    """商家管理类, 单例"""

    def __init__(self):
        # 用于存储所有商家对象
        self.SList = []
        # 商家号 -> 商家对象
        self.sellerSID = {}

        self.load()

        self.emptySeller = Seller()

    def add(self, seller):
        seller.SID = str(random.randint(0,999)).rjust(3, '0')
        while(sql.check_user(seller.SID, seller)[0] == False):
            seller.SID = str(random.randint(0,999)).rjust(3, '0')
        self.SList.append(seller)
        self.sellerSID[seller.SID] = seller
        return sql.seller_add(seller)

    def delete(self, seller):
        self.sellerSID.pop(seller.SID)
        self.SList.remove(seller)
        sql.seller_delete(seller)
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
        msg = sql.Seller_multiselect(searchBy, keyText)
        #print(searchBy)
        #print(keyText)
        result = self.toSeller(msg)
        return result

    def search(self, searchBy, keyList):
        #print(searchBy)
        result = []
        if not keyList:
            result = self.load()
            return result
        else:
            msg = sql.Seller_select(searchBy, keyList)
            result = result + self.toSeller(msg)
            # print(result)
            return result

    def toSeller(self,msg):
        result = []
        for i in range(len(msg)):
            # 创建每一个数据的Seller对象
            m = msg[i]
            # print(s)
            seller = Seller()
            seller.SID = m[0]
            seller.Sname = m[1]
            seller.Saddr = m[2]
            seller.Sphone = m[3]
            result.append(seller)
        return result

    def load(self):
        SList = []
        sellerSID = {}
        try:
            msg = sql.Load("s_table")
            result = self.toSeller(msg)
            for seller in result:
                SList.append(seller)
                sellerSID[seller.SID] = seller
            result = True
        except:
            result = False
        finally:
            self.SList = SList
            self.sellerSID = sellerSID

        #print(self.MMID)
        #print(self.MList)
        return SList
    
class Seller(object):
    """商家类, 用于存储商家基本信息"""
    def __init__(self, SID="", Sname="", Saddr="", Sphone=""):
        self.SID = SID
        self.Sname = Sname
        self.Saddr = Saddr
        self.Sphone = Sphone

    def copy(self):
        seller = Seller()
        self.copyTo(seller)
        return seller

    def copyTo(self, seller):
        seller.SID = self.SID
        seller.Sname = self.Sname
        seller.Saddr = self.Saddr
        seller.Sphone = self.Sphone

    def checkInfo(self,new=False):
        '''检查自身信息是否完整合法'''
        # 空值检测
        for attr, text in attributeList_seller:
            if not getattr(self, attr):
                return (False, "%s不能为空" % text)
        # 重复性检测
        check = sql.check_seller(self.SID, new)
        if check[0] ==0:
            return check

        return (True, "")
