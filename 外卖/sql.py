import pymysql

def open():
    # 打开数据库连接
    db = pymysql.connect(host="127.0.0.1", user="root", db="mysql")
    return db


def Load(table):
    #加载table表的全部信息
    db = open()
    cursor = db.cursor()
    sql = "select * from {}".format(table)

    # 执行SQL语句
    cursor.execute(sql)
    results = cursor.fetchall()
    # 关闭数据库连接
    db.close()
    return results


# 订单
def check_order(OID, Uaddress, Uphone, Saddress, Sphone, Rphone, Rname, Ostate, new):
    flag = True
    msg = ''
    db = open()
    cursor = db.cursor()
    sql1 = "select Uaddress from user_table where Uaddress = {}".format(Uaddress)
    sql2 = "select Uphone from user_table where Uphone = {}".format(Uphone)
    sql3 = "select Saddress from seller_table where Saddress = {}".format(Saddress)
    sql4 = "select Sphone from seller_table where Sphone = {}".format(Sphone)
    sql5 = "select Rphone from rider_table where Rphone = {}".format(Rphone)
    sql6 = "select Rname from rider_table where Rname = {}".format(Rname)
    sql7 = "select OID from order_table where OID = {}".format(OID)

    cursor.execute(sql1)
    results1 = cursor.fetchall()
    cursor.execute(sql2)
    results2 = cursor.fetchall()
    cursor.execute(sql3)
    results3 = cursor.fetchall()
    cursor.execute(sql4)
    results4 = cursor.fetchall()
    cursor.execute(sql5)
    results5 = cursor.fetchall()
    cursor.execute(sql6)
    results6 = cursor.fetchall()
    cursor.execute(sql7)
    results7 = cursor.fetchall()

    if results1 == ():
        msg += '不存在该用户地址、'
        flag = False
    
    if results2 == ():
        msg += '不存在该用户电话、'
        flag = False

    if results3 == ():
        msg += '不存在该商家地址、'
        flag = False
    
    if results4 == ():
        msg += '不存在该商家电话、'
        flag = False

    if results5 == ():
        msg += '不存在该骑手、'
        flag = False

    if results6 == ():
        msg += '不存在该骑手、'
        flag = False

    if results7 != () and new:
        msg += '订单号重复、'
        flag = False

    db.close()
    return (flag,msg)

def order_add(order):
    #增加订单
    db = open()
    cursor = db.cursor()
    sql1 = """insert into order_table(OID,Uaddress,Uphone,Saddress,Sphone,Rphone,Rname,Ostate)
                values ("{}","{}",{},"{}","{}","{}","{}")""".format(order.OID, order.Uaddress, order.Uphone, order.Saddress, order.Sphone, order.Rphone, order.Rname, order.Ostate)
    try:
        # 执行SQL语句
        cursor.execute(sql1)
    except Exception as e:
        db.rollback()  # 事务回滚
        print('增加订单失败', e)
        flag = (False, e)
    else:
        db.commit()  # 事务提交
        print('增加订单成功', cursor.rowcount)
        flag = (True, "")

    # 关闭数据库连接
    db.close()
    return flag

def order_delete(order):
    db = open()
    cursor = db.cursor()
    sql1 = "delete from order_table where OID = {}".format(order.OID)
    try:
        # 执行SQL语句
        cursor.execute(sql1)
    except Exception as e:
        db.rollback()  # 事务回滚
        print('删除订单失败', e)
    else:
        db.commit()  # 事务提交
        print('删除订单成功', cursor.rowcount)

    # 关闭数据库连接
    db.close()

def order_select(seachby, keyList):
    #订单单属性查询
    db = open()
    cursor = db.cursor()
    sql1 = "select * from order_table where {} REGEXP '{}' ".format(seachby, keyList)
    try:
        # 执行SQL语句
        cursor.execute(sql1)
    except Exception as e:
        results = ()
        db.rollback()  # 事务回滚
        print('查询订单失败', e)
    else:
        results = cursor.fetchall()
        print('查询订单成功', cursor.rowcount)

    # 关闭数据库连接
    db.close()
    return results

def order_multiselect(seachby, keyList):
    #订单多属性查询
    db = open()
    cursor = db.cursor()
    sql1 = "select * from order_table "
    for i in range(len(seachby)):
        if i == 0:
            sql1 = sql1 + "where {} REGEXP '{}' ".format(seachby[i],keyList[i])
        else:
            sql1 = sql1 + "and {} REGEXP '{}' ".format(seachby[i], keyList[i])
    try:
        # 执行SQL语句
        cursor.execute(sql1)
    except Exception as e:
        results = ()
        db.rollback()  # 事务回滚
        print('查询订单失败', e)
    else:
        results = cursor.fetchall()
        print('查询订单成功', cursor.rowcount)

    # 关闭数据库连接
    db.close()
    return results


# 用户
def check_user(UID, new):
    flag = True
    msg = ''
    db = open()
    cursor = db.cursor()
    sql = "select UID from user_table where UID = {}".format(UID)
    cursor.execute(sql)
    results1 = cursor.fetchall()
    if results1 != () and new:
        msg += '已有该用户'
        flag =False
    db.close()
    return (flag,msg)

def user_add(user):
    db = open()
    cursor = db.cursor()
    sql1 = """insert into user_table(UID,Uname,Uaddress,Uphone)
                values ("{}","{}","{}","{}")""".format(user.UID, user.Uname, user.Uaddress, user.Uphone)
    print(sql1)
    try:
        cursor.execute(sql1)
    except Exception as e:
        db.rollback()
        print('增加用户失败', e)
        flag = (False, e)
    else:
        db.commit()
        print('增加用户成功', cursor.rowcount)
        flag = (True, "")

    db.close()
    return flag

def user_delete(user):
    db = open()
    cursor = db.cursor()
    sql1 = "delete from user_table where UID = {}".format(user.UID)
    try:
        cursor.execute(sql1)
    except Exception as e:
        db.rollback() 
        print('删除用户失败', e)
        flag = (False, e)
    else:
        db.commit()  
        print('删除用户成功', cursor.rowcount)
        flag = (True, "")
        
    db.close()
    return flag

def user_select(seachby, keyList):
    db = open()
    cursor = db.cursor()
    sql1 = "select * from user_table where {} REGEXP '{}' ".format(seachby, keyList)
    try:
        cursor.execute(sql1)
    except Exception as e:
        results = ()
        db.rollback()
        print('查询用户失败', e)
    else:
        results = cursor.fetchall()
        print('查询用户成功', cursor.rowcount)

    db.close()
    return results

def user_multiselect(seachby, keyList):
    db = open()
    cursor = db.cursor()
    sql1 = "select * from user_table "
    for i in range(len(seachby)):
        if i == 0:
            sql1 = sql1 + "where {} REGEXP '{}' ".format(seachby[i],keyList[i])
        else:
            sql1 = sql1 + "and {} REGEXP '{}' ".format(seachby[i], keyList[i])
    try:
        cursor.execute(sql1)
    except Exception as e:
        results = ()
        db.rollback()
        print('查询用户失败', e)
    else:
        results = cursor.fetchall()
        print('查询用户成功', cursor.rowcount)

    db.close()
    return results


# 商家
def check_seller(SID, new):
    flag = True
    msg = ''
    db = open()
    cursor = db.cursor()
    sql = "select UID from seller_table where SID = {}".format(SID)
    cursor.execute(sql)
    results1 = cursor.fetchall()
    if results1 != () and new:
        msg += '已有该商家'
        flag =False
    db.close()
    return (flag,msg)

def seller_add(seller):
    db = open()
    cursor = db.cursor()
    sql1 = """insert into seller_table(SID,Sname,Saddress,Sphone)
                values ("{}","{}",{},"{}")""".format(seller.SID, seller.Sname, seller.Saddress, seller.Sphone)
    try:
        cursor.execute(sql1)
    except Exception as e:
        db.rollback()
        print('增加商家失败', e)
        flag = (False, e)
    else:
        db.commit()
        print('增加商家成功', cursor.rowcount)
        flag = (True, "")

    db.close()
    return flag

def seller_delete(seller):
    db = open()
    cursor = db.cursor()
    sql1 = "delete from seller_table where SID = {}".format(seller.SID)
    try:
        cursor.execute(sql1)
    except Exception as e:
        db.rollback() 
        print('删除商家失败', e)
    else:
        db.commit()  
        print('删除商家成功', cursor.rowcount)

    db.close()

def seller_select(seachby, keyList):
    db = open()
    cursor = db.cursor()
    sql1 = "select * from seller_table where {} REGEXP '{}' ".format(seachby, keyList)
    try:
        cursor.execute(sql1)
    except Exception as e:
        results = ()
        db.rollback()
        print('查询商家失败', e)
    else:
        results = cursor.fetchall()
        print('查询商家成功', cursor.rowcount)

    db.close()
    return results

def seller_multiselect(seachby, keyList):
    db = open()
    cursor = db.cursor()
    sql1 = "select * from seller_table "
    for i in range(len(seachby)):
        if i == 0:
            sql1 = sql1 + "where {} REGEXP '{}' ".format(seachby[i],keyList[i])
        else:
            sql1 = sql1 + "and {} REGEXP '{}' ".format(seachby[i], keyList[i])
    try:
        cursor.execute(sql1)
    except Exception as e:
        results = ()
        db.rollback()
        print('查询商家失败', e)
    else:
        results = cursor.fetchall()
        print('查询商家成功', cursor.rowcount)

    db.close()
    return results


# 骑手
def check_rider(RID, new):
    flag = True
    msg = ''
    db = open()
    cursor = db.cursor()
    sql = "select RID from rider_table where RID = {}".format(RID)
    cursor.execute(sql)
    results1 = cursor.fetchall()
    if results1 != () and new:
        msg += '已有该骑手'
        flag =False
    db.close()
    return (flag,msg)

def rider_add(rider):
    db = open()
    cursor = db.cursor()
    sql1 = """insert into rider_table(RID,Rname,Rphone)
                values ("{}","{}",{})""".format(rider.RID, rider.Rname, rider.Rphone)
    try:
        cursor.execute(sql1)
    except Exception as e:
        db.rollback()
        print('增加骑手失败', e)
        flag = (False, e)
    else:
        db.commit()
        print('增加骑手成功', cursor.rowcount)
        flag = (True, "")

    db.close()
    return flag

def rider_delete(rider):
    db = open()
    cursor = db.cursor()
    sql1 = "delete from rider_table where RID = {}".format(rider.RID)
    try:
        cursor.execute(sql1)
    except Exception as e:
        db.rollback() 
        print('删除骑手失败', e)
    else:
        db.commit()  
        print('删除骑手成功', cursor.rowcount)

    db.close()

def rider_select(seachby, keyList):
    db = open()
    cursor = db.cursor()
    sql1 = "select * from rider_table where {} REGEXP '{}' ".format(seachby, keyList)
    try:
        cursor.execute(sql1)
    except Exception as e:
        results = ()
        db.rollback()
        print('查询骑手失败', e)
    else:
        results = cursor.fetchall()
        print('查询骑手成功', cursor.rowcount)

    db.close()
    return results

def rider_multiselect(seachby, keyList):
    db = open()
    cursor = db.cursor()
    sql1 = "select * from rider_table "
    for i in range(len(seachby)):
        if i == 0:
            sql1 = sql1 + "where {} REGEXP '{}' ".format(seachby[i],keyList[i])
        else:
            sql1 = sql1 + "and {} REGEXP '{}' ".format(seachby[i], keyList[i])
    try:
        cursor.execute(sql1)
    except Exception as e:
        results = ()
        db.rollback()
        print('查询骑手失败', e)
    else:
        results = cursor.fetchall()
        print('查询骑手成功', cursor.rowcount)

    db.close()
    return results