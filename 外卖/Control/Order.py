import sql
import random
# 订单属性集
attributeList_order = [
    ("OID","订单号"),
    ("UID","用户号"),
    ("SID","商家号"),
    ("RID","骑手号")
]

class OrderManager(object):
    """订单管理类, 单例"""

    def __init__(self):
        # 用于存储所有订单对象
        self.OList = []
        # 订单号 -> 订单对象
        self.order_OID = {}

        self.load()

        self.emptyOrder = Order()

    def add(self, order):
        order.OID = str(random.randint(0,999)).rjust(3, '0')
        while(sql.check_user(order.OID, order)[0] == False):
            order.OID = str(random.randint(0,999)).rjust(3, '0')
        self.OList.append(order)
        self.order_OID[order.OID] = order
        return sql.order_add(order)

    def delete(self, order):
        self.order_OID.pop(order.OID)
        self.OList.remove(order)
        return sql.order_delete(order)
    
    def edit(self, status):
        self.status = status

    def multiSearch(self, keyList):
        
        def check(o1, o2):
            return o1.OID == o2.OID
        def check_in(o, OL):
            for ol in OL:
                if check(o, ol):
                    return True
            return False
        
        # print(keyList)
        searchBy = []
        keyText = []
        #print(keyList)
        for searchby, keytext in keyList:
            if keytext:
                searchBy.append(searchby)
                keyText.append(keytext)
        msgs = sql.order_search(searchBy, keyText)
        print("msgs: ", msgs)
        # exit()
        def get_msg(itemlist):
            res = []
            for item in itemlist:
                tmp = Order(item[0], item[1], item[2], item[3])
                res.append(tmp)
            return res

        temp = [get_msg(msg) for msg in msgs]

        result = []
        if len(temp) == 0:
            return result
        for item in temp[0]:
            print("item:", item.OID, item.UID, item.SID, item.RID)
            ok = True
            for i in range(1, len(temp)):
                if not check_in(item, temp[i]):
                    ok = False
                    break
            if ok:
                result.append(item)
        print('result: ', result)
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
            # print(m)
            order = Order()
            order.OID = m[0]
            order.UID = m[1]
            order.SID = m[2]
            order.RID = m[3]
            result.append(order)
        return result

    def load(self):
        OList = []
        order_OID = {}
        try:
            msg = sql.Load("order_table")
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
    def __init__(self, OID = "", UID = "", SID = "", RID = ""):
        self.OID = OID
        self.UID = UID
        self.SID = SID
        self.RID = RID
        
    def copy(self):
        order = Order()
        self.copyTo(order)
        return order

    def copyTo(self, order):
        order.OID = self.OID
        order.UID = self.UID
        order.SID = self.SID
        order.RID = self.RID


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
