import sql
import random
# 订单属性集
attributeList_order = [
    ("OID","订单号"),
    ("Saddr","商家地址"),
    ("Sphone","商家电话"),
    ("Uaddr", "配送地址"),
    ("Uphone", "用户电话")
]

class OrderManager(object):
    """订单管理类, 单例"""

    def __init__(self):
        # 用于存储所有订单对象
        self.OList = []
        # 订单号 -> 订单对象
        self.order_OID = {}

        # 订单状态： 0 -> None, 1 -> 商家已接单, 2 -> 订单已送达
        self.status = 0

        self.load()

        self.emptyOrder = Order()

    def add(self, order):
        order.SID = str(random.randint(0,999)).rjust(3, '0')
        while(sql.check_user(order.SID, order)[0] == False):
            order.SID = str(random.randint(0,999)).rjust(3, '0')
        self.OList.append(order)
        self.order_OID[order.OID] = order
        return sql.order_add(order)

    def delete(self, order):
        self.order_OID.pop(order.OID)
        self.OList.remove(order)
        sql.order_delete(order)
        return True
    
    def edit(self, status):
        self.status = status

    def multiSearch(self, keyList):
        # print(keyList)
        searchBy = []
        keyText = []
        #print(keyList)
        for searchby, keytext in keyList:
            if keytext:
                searchBy.append(searchby)
                keyText.append(keytext)
        msg = sql.order_multiselect(searchBy, keyText)
        #print(searchBy)
        #print(keyText)
        result = self.toorder(msg)
        return result

    def search(self, searchBy, keyList):
        #print(searchBy)
        result = []
        if not keyList:
            result = self.load()
            return result
        else:
            msg = sql.order_select(searchBy, keyList)
            result = result + self.toorder(msg)
            return result

    def toorder(self,msg):
        result = []
        for i in range(len(msg)):
            # 创建每一个数据的order对象
            m = msg[i]
            # print(s)
            order = Order()
            order.OID = m[0]
            order.Saddr = m[1]
            order.Sphone = m[2]
            order.Uaddr = m[3]
            order.Uphone = m[4]
            result.append(order)
        return result

    def load(self):
        OList = []
        order_OID = {}
        try:
            msg = sql.Load("m_table")
            result = self.toorder(msg)
            for order in result:
                OList.append(order)
                order_OID[order.OID] = order
            result = True
        except:
            result = False
        finally:
            self.OList = OList
            self.order_OID = order_OID

        #print(self.MMID)
        #print(self.MList)
        return OList
    
class Order(object):
    """订单类, 用于存储订单基本信息"""
    def __init__(self, OID="", Saddr="", Sphone="", Uaddr="", Uphone="", Rname="", Rphone = ""):
        self.OID = OID
        self.Saddr = Saddr
        self.Sphone = Sphone
        self.Uaddr = Uaddr
        self.Uphone = Uphone
        self.Rname = Rname
        self.Rphone = Rphone
        
    def copy(self):
        order = Order()
        self.copyTo(order)
        return order

    def copyTo(self, order):
        order.OID = self.OID
        order.Saddr = self.Saddr
        order.Sphone = self.Sphone
        order.Uaddr = self.Uaddr
        order.Uphone = self.Uphone
        order.Rname = self.Rname
        order.Rphone = self.Rphone

    def checkInfo(self,new=False):
        '''检查自身信息是否完整合法'''
        # 空值检测
        for attr, text in attributeList_order:
            if not getattr(self, attr):
                return (False, "%s不能为空" % text)
        # 重复性检测
        check = sql.check_order(self.OID, new)
        if check[0] ==0:
            return check

        return (True, "")
