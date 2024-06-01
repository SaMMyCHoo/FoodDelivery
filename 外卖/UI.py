import tkinter as tk
from tkinter import ttk
from Control.User import UserManager, User
from Control.Rider import RiderManager, Rider
from Control.Seller import SellerManager, Seller
from Control.Order import OrderManager, Order

help_text = '''
这是一个外卖管理系统，主要负责管理用户，商家，骑手以及他们之间的订单数据。
通过左上角的选项卡可以切换不同的对象，并输入信息完成相应的操作。
查询操作可以任意输入内容，也可以不输入，若不输入则显示所有内容。
添加操作需要填写除ID以外的所有信息，ID由系统自动分配。
删除操作则仅需要填写ID信息。
祝您使用愉快！
'''

class DatabaseUI:
    def __init__(self, master):
        self.master = master
        self.master.title("外卖管理系统")
        
        self.user_sys = UserManager()
        self.seller_sys = SellerManager()
        self.rider_sys = RiderManager()
        self.order_sys = OrderManager()

        # 创建帮助Frame
        self.help_frame = tk.Frame(master)
        self.help_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        # 添加使用说明按钮
        self.help_button = tk.Button(self.help_frame, text="显示使用说明", command=self.toggle_help_text)
        self.help_button.pack(side="left", pady=(0, 10))
        
        # 添加使用说明标签（初始隐藏）
        self.help_text_content = help_text
        self.help_text = tk.Label(self.help_frame, text=self.help_text_content, wraplength=600, justify="left")
        self.help_text.pack(side="left", pady=(0, 10))
        self.help_text.pack_forget()
        
        # 使用说明显示状态
        self.is_help_text_visible = False

        # 创建选项卡
        self.tabControl = ttk.Notebook(master)
        
        # 初始化输入框
        self.input_fields = {}
        self.result_trees = dict()
        
        # 创建用户管理选项卡
        self.create_tab(self.tabControl, "用户", ["用户ID", "昵称", "用户地址", "手机"])
        
        # 创建商家管理选项卡
        self.create_tab(self.tabControl, "商家", ["商家ID", "商家名称", "商家地址", "电话"])
        
        # 创建骑手管理选项卡
        self.create_tab(self.tabControl, "骑手", ["骑手ID", "骑手名称", "联系方式"])
        
        # 创建订单管理选项卡
        self.create_tab(self.tabControl, "订单", ["订单ID", "配送地址", "用户电话", "店家地址", "商家电话", "骑手姓名", "骑手电话"])
        
        self.tabControl.pack(expand=1, fill="both")
        
        # 添加文本输出框
        self.info_text = tk.Text(master, height=5)
        self.info_text.pack(fill="x", padx=10, pady=(0, 10))        

        # 绑定选项卡切换事件
        self.tabControl.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def toggle_help_text(self):
        if self.is_help_text_visible:
            self.help_text.pack_forget()
            self.help_button.config(text="显示使用说明")
        else:
            self.help_text.pack(side="left", pady=(0, 10))
            self.help_button.config(text="隐藏使用说明")
        self.is_help_text_visible = not self.is_help_text_visible
  
    def create_tab(self, tab_control, entity, input_fields):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text=entity)
        
        label = tk.Label(tab, text=f"管理{entity}：")
        label.pack(pady=10)
        
        # 创建独立的Treeview对象
        result_tree = ttk.Treeview(tab, columns=tuple(input_fields))
        for field in input_fields:
            result_tree.heading(field, text=field)
        result_tree.pack(pady=10)
        result_tree["show"] = "headings"
        
        input_frame = tk.Frame(tab)  # 创建一个新的输入框容器
        input_frame.pack(pady=10)
        
        self.create_input_frame(input_frame, input_fields)
        self.create_buttons(tab)
        
        # 保存Treeview对象到类属性中
        self.result_trees[entity] = result_tree

    def create_input_frame(self, parent, fields):
        for i, field in enumerate(fields):
            tk.Label(parent, text=f"{field}：").grid(row=i, column=0, padx=5, pady=5, sticky="e")
            self.input_fields[field] = tk.Entry(parent)
            self.input_fields[field].grid(row=i, column=1, padx=5, pady=5)
        
    def create_buttons(self, parent):
        button_frame = tk.Frame(parent)
        button_frame.pack(pady=10)
        
        self.query_button = tk.Button(button_frame, text="查询", command=self.query)
        self.query_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.add_button = tk.Button(button_frame, text="添加", command=self.add)
        self.add_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.delete_button = tk.Button(button_frame, text="删除", command=self.delete)
        self.delete_button.grid(row=0, column=2, padx=5, pady=5)
        
    def query(self):
        current_tab = self.tabControl.tab(self.tabControl.select(), "text")  # 获取当前选项卡的文本
        input_values = {}
        for field, entry in self.input_fields.items():
            input_values[field] = entry.get()
            
        current_tree = self.result_trees[current_tab]
        
        if current_tab == "用户":
            # 执行用户查询操作
            id = input_values["用户ID"]
            name = input_values["昵称"]
            address = input_values["用户地址"]
            phone = input_values["手机"]
            keylist = []
            if id != '':
                keylist.append(("UID", id))
            if name != '':
                keylist.append(("Uname", name))
            if address != '':
                keylist.append(("Uaddress", address))
            if phone!= '':
                keylist.append(("Uphone", phone))
            # print(name)
            res=[]
            temp = self.user_sys.multiSearch(keylist)
            for i in range(len(temp)):
                now = temp[i]
                new = (now.UID, now.Uname, now.Uaddress, now.Uphone)
                res.append(new)
        elif current_tab == "商家":
            # 执行商家查询操作
            id = input_values["商家ID"]
            name = input_values["商家名称"]
            address = input_values["商家地址"]
            phone = input_values["电话"]
            keylist = []
            if id != '':
                keylist.append(('SID', id))
            if name != '':
                keylist.append(("Sname", name))
            if address != '':
                keylist.append(("Saddress", address))
            if phone!= '':
                keylist.append(("Sphone", phone))
            temp = self.seller_sys.multiSearch(keylist)
            res=[]
            for i in range(len(temp)):
                now = temp[i]
                new = (now.SID, now.Sname, now.Saddr, now.Sphone)
                res.append(new)
        elif current_tab == "骑手":
            # 执行骑手查询操作
            id = input_values["骑手ID"]
            name = input_values["骑手名称"]
            phone = input_values["联系方式"]
            keylist = []
            if id != '':
                keylist.append(("RID", id))
            if name != '':
                keylist.append(("Rname", name))
            if phone!= '':
                keylist.append(("Rphone", phone))
            temp = self.rider_sys.multiSearch(keylist)
            res=[]
            for i in range(len(temp)):
                now = temp[i]
                new = (now.RID, now.Rname, now.Rphone)
                print(new)
                res.append(new)
        elif current_tab == "订单":
            # 执行订单查询操作
            id = input_values["订单ID"]
            user_address = input_values["配送地址"]
            user_phone = input_values["用户电话"]
            seller_address = input_values["店家地址"]
            seller_phone = input_values["商家电话"]
            rider_name = input_values["骑手姓名"]
            rider_phone = input_values["骑手电话"]
            keylist = []
            if id != '':
                keylist.append(("OID", id))
            if user_address != '':
                keylist.append(("Uaddress", user_address))
            if user_phone != '':
                keylist.append(("Uphone", user_phone))
            if seller_address != '':
                keylist.append(("Saddress", seller_address))
            if seller_phone != '':
                keylist.append(("Sphone", seller_phone))
            if rider_name != '':
                keylist.append(("Rname", rider_name))
            if rider_phone != '':
                keylist.append(("Rphone", rider_phone))
            temp = self.order_sys.multiSearch(keylist)
            res=[]
            for i in range(len(temp)):
                now = temp[i]
                new = (now.OID, now.Uaddr, now.Uphone, now.Saddr, now.Sphone, now.Rname, now.Rphone)
                print(new)
                res.append(new)

        current_tree.delete(*current_tree.get_children())
        for item in res:
            current_tree.insert('', 'end', text='', values=item)
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, f"查询到{len(res)}个结果。")
    
    def add(self):

        def check_user(address, phone):
            if address == "":
                return False
            if phone == "":
                return False
            for user in self.user_sys.userList:
                print('1', user.Uaddress)
                print('2', user.Uphone)
                if (user.Uaddress == address) and (user.Uphone == phone):
                    return True        
            return False
            
        def check_seller(address, phone):
            if address == "":
                return False
            if phone == "":
                return False
            for seller in self.seller_sys.SList:
                if (seller.Saddr == address) and (seller.Sphone == phone):
                    return True        
            return False        
        
        def check_rider(name, phone):
            if name == "":
                return False
            if phone == "":
                return False
            for rider in self.rider_sys.RList:
                if (rider.Rname == name) and (rider.Rphone == phone):
                    return True        
            return False        
            
        current_tab = self.tabControl.tab(self.tabControl.select(), "text")  # 获取当前选项卡的文本
        
        input_values = {}
        for field, entry in self.input_fields.items():
            input_values[field] = entry.get()

        current_tree = self.result_trees[current_tab]
        output = []
        
        def check(now):
            if current_tab == '用户':
                name = now.Uname
                addr = now.Uaddress
                phone = now.Uphone
                if name == '':
                    return False
                if addr == '':
                    return False
                if phone == '':
                    return False
                for user in self.user_sys.userList:
                    if (user.Uname == name) and (user.Uaddress == addr) and (user.Uphone == phone):
                        return False
                return True
            elif current_tab == '商家':
                name = now.Sname
                addr = now.Saddr
                phone = now.Sphone
                if name == '':
                    return False
                if addr == '':
                    return False
                if phone == '':
                    return False
                for user in self.seller_sys.SList:
                    if (user.Sname == name) and (user.Saddr == addr) and (user.Sphone == phone):
                        return False
                return True          
            elif current_tab == '骑手':
                name = now.Rname
                phone = now.Rphone
                if name == '':
                    return False
                if phone == '':
                    return False
                for user in self.rider_sys.RList:
                    if (user.Rname == name) and (user.Rphone == phone):
                        return False
                return True
            else:
                return False
                

        print("Input values:", input_values)  # 打印输入的值
        if current_tab == "用户":
            # 执行用户添加操作
            name = input_values["昵称"]
            address = input_values["用户地址"]
            phone = input_values["手机"]
            temp = User(Uname = name, Uaddr = address, Uphone = phone)
            if not check(temp):
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "添加失败：用户信息不完整或已存在！") 
                return
            res = self.user_sys.add(temp)
            temp = self.user_sys.multiSearch([])            
            for i in range(len(temp)):
                now = temp[i]
                new = (now.UID, now.Uname, now.Uaddr, now.Uphone)
                output.append(new)

        elif current_tab == "商家":
            # 执行商家添加操作     
            name = input_values["商家名称"]
            address = input_values["商家地址"]
            phone = input_values["电话"]
            temp = Seller(Sname = name, Saddr = address, Sphone = phone)
            if not check(temp):
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "添加失败：商家信息不完整或已存在！") 
                return
            res = self.seller_sys.add(temp)
            temp = self.seller_sys.multiSearch([])            
            for i in range(len(temp)):
                now = temp[i]
                new = (now.SID, now.Sname, now.Saddr, now.Sphone)
                output.append(new)
                
        elif current_tab == "骑手":
            # 执行骑手添加操作
            name = input_values["骑手名称"]
            phone = input_values["联系方式"]
            temp = Rider(Rname = name, Rphone = phone)
            if not check(temp):
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "添加失败：骑手信息不完整或已存在！") 
                return
            res = self.rider_sys.add(temp)
            temp = self.rider_sys.multiSearch([])            
            for i in range(len(temp)):
                now = temp[i]
                new = (now.RID, now.Rname, now.Rphone)
                output.append(new)
            
        elif current_tab == "订单":
            # 执行订单添加操作
            # "配送地址", "用户电话", "店家地址", "商家电话", "骑手姓名", "骑手电话"
            user_address = input_values["配送地址"]
            user_phone = input_values["用户电话"]
            seller_address = input_values["店家地址"]
            seller_phone = input_values["商家电话"]
            rider_name = input_values["骑手姓名"]
            rider_phone = input_values["骑手电话"]
            
            if not check_user(user_address, user_phone):
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "添加失败：用户信息不完整或不存在！")
                return
            
            if not check_seller(seller_address, seller_phone):
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "添加失败：商家信息不完整或不存在！")
                return

            if not check_rider(rider_name, rider_phone):
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "添加失败：骑手信息不完整或不存在！")
                return

            temp = Order(Uaddr = user_address, 
                         Uphone = user_phone, 
                         Saddr = seller_address, 
                         Sphone = seller_phone, 
                         Rname = rider_name,
                         Rphone = rider_phone)
            res = self.order_sys.add(temp)   
            temp = self.order_sys.multiSearch([])
            for i in range(len(temp)):
                now = temp[i]
                new = (now.OID, now.Uaddr, now.Uphone, now.Saddr, now.Sphone, now.Rname, now.Rphone)
                print(new)
                output.append(new)
        if res[0]:
            current_tree.delete(*current_tree.get_children())
            for item in output:
                current_tree.insert('', 'end', text='', values=item)
            self.info_text.delete("1.0", tk.END)
            self.info_text.insert(tk.END, "添加成功！")
        else:
            self.info_text.delete("1.0", tk.END)
            self.info_text.insert(tk.END, "添加失败：" + str(res[1]))      
        
    def delete(self):
        
        current_tab = self.tabControl.tab(self.tabControl.select(), "text")  # 获取当前选项卡的文本
        
        def check(id):
            if current_tab == '用户':
                return (id in self.user_sys.userUID.keys())
            elif current_tab == '商家':
                return (id in self.seller_sys.sellerSID.keys())
            elif current_tab == '骑手':
                return (id in self.rider_sys.rider_RID.keys())
            else:
                return (id in self.order_sys.order_OID.keys())
            
        input_values = {}
        for field, entry in self.input_fields.items():
            input_values[field] = entry.get()

        current_tree = self.result_trees[current_tab]
        output = []

        if current_tab == "用户":
            # 执行用户删除操作
            user_id = input_values["用户ID"]
            if not check(user_id):
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除失败：用户ID不存在！")
                return
            res = self.user_sys.delete(self.user_sys.userUID[user_id])
            if res[0]:
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除成功！")
            else:
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除失败：" + res[1])
            temp = self.user_sys.multiSearch([])            
            for i in range(len(temp)):
                now = temp[i]
                new = (now.UID, now.Uname, now.Uaddress, now.Uphone)
                output.append(new)
            
        elif current_tab == "商家":
            # 执行商家删除操作
            seller_id = input_values["商家ID"]
            if not check(seller_id):
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除失败：商家ID不存在！")
                return
            res = self.seller_sys.delete(self.seller_sys.sellerSID[seller_id])
            if res[0]:
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除成功！")
            else:
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除失败：" + res[1])
            temp = self.seller_sys.multiSearch([])            
            for i in range(len(temp)):
                now = temp[i]
                new = (now.SID, now.Sname, now.Saddr, now.Sphone)
                output.append(new)
        elif current_tab == "骑手":
            # 执行骑手删除操作
            rider_id = input_values["骑手ID"]
            if not check(rider_id):
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除失败：骑手ID不存在！")
                return
            res = self.rider_sys.delete(self.rider_sys.rider_RID[rider_id])
            if res[0]:
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除成功！")
            else:
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除失败：" + res[1])
            temp = self.rider_sys.multiSearch([])            
            for i in range(len(temp)):
                now = temp[i]
                new = (now.RID, now.Rname, now.Rphone)
                output.append(new)
        elif current_tab == "订单":
            # 执行订单删除操作
            # print(self.order_sys.order_OID)

            order_id = input_values["订单ID"]
            if not check(order_id):
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除失败：订单ID不存在！")
                return
            res = self.order_sys.delete(self.order_sys.order_OID[order_id])
            if res[0]:
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除成功！")
            else:
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除失败：" + res[1])
            temp = self.order_sys.multiSearch([])
            for i in range(len(temp)):
                now = temp[i]
                new = (now.OID, now.Uaddr, now.Uphone, now.Saddr, now.Sphone, now.Rname, now.Rphone)
                print(new)
                output.append(new)
        
        current_tree.delete(*current_tree.get_children())
        for item in output:
            current_tree.insert('', 'end', text='', values=item)

    def on_tab_changed(self, event):
        # 当选项卡切换时调用此方法
        
        current_tab = self.tabControl.tab(self.tabControl.select(), "text")  # 获取当前选项卡的文本
            
        input_values = {}
        for field, entry in self.input_fields.items():
            input_values[field] = entry.get()

        current_tree = self.result_trees[current_tab]
        output = []

        if current_tab == "用户":
            temp = self.user_sys.multiSearch([])           
            for i in range(len(temp)):
                now = temp[i]
                new = (now.UID, now.Uname, now.Uaddress, now.Uphone)
                output.append(new)    
        elif current_tab == "商家":
            temp = self.seller_sys.multiSearch([])            
            for i in range(len(temp)):
                now = temp[i]
                new = (now.SID, now.Sname, now.Saddr, now.Sphone)
                output.append(new)
        elif current_tab == "骑手":
            temp = self.rider_sys.multiSearch([])            
            for i in range(len(temp)):
                now = temp[i]
                new = (now.RID, now.Rname, now.Rphone)
                output.append(new)
        elif current_tab == "订单":
            temp = self.order_sys.multiSearch([])
            for i in range(len(temp)):
                now = temp[i]
                new = (now.OID, now.Uaddr, now.Uphone, now.Saddr, now.Sphone, now.Rname, now.Rphone)
                output.append(new)
        
        current_tree.delete(*current_tree.get_children())
        for item in output:
            current_tree.insert('', 'end', text='', values=item)

        # 清空输入框内容
        for entry in self.input_fields.values():
            entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = DatabaseUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
