import tkinter as tk
from tkinter import ttk
from Control.User import UserManager, User
from Control.Rider import RiderManager, Rider
from Control.Seller import SellerManager, Seller
from Control.Order import OrderManager, Order

class DatabaseUI:
    def __init__(self, master):
        self.master = master
        self.master.title("外卖管理系统")
        
        self.user_sys = UserManager()
        self.seller_sys = SellerManager()
        self.rider_sys = RiderManager()
        self.order_sys = OrderManager()
        
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
        current_tree.delete(*current_tree.get_children())
        
        if current_tab == "用户":
            # 执行用户查询操作
            name = input_values["昵称"]
            address = input_values["用户地址"]
            phone = input_values["手机"]
            keylist = []
            if name != '':
                keylist.append(("Uname", name))
            if address != '':
                keylist.append(("Uaddress", address))
            if phone!= '':
                keylist.append(("Uphone", phone))
            # print(name)
            res = self.user_sys.multiSearch(keylist)
            # print(res)
            # res = [
            # ('1', 'John', '123 Main St', '123-456-7890'),
            # ('2', 'Alice', '456 Oak Ave', '987-654-3210')
            # ]
        elif current_tab == "商家":
            # 执行商家查询操作
            name = input_values["商家名称"]
            address = input_values["商家地址"]
            phone = input_values["电话"]
            keylist = []
            if name != '':
                keylist.append(("Sname", name))
            if address != '':
                keylist.append(("Saddress", address))
            if phone!= '':
                keylist.append(("Sphone", phone))
            res = self.user_sys.multiSearch(keylist)
        elif current_tab == "骑手":
            # 执行骑手查询操作
            name = input_values["骑手名称"]
            phone = input_values["联系方式"]
            keylist = []
            if name != '':
                keylist.append(("Rname", name))
            if phone!= '':
                keylist.append(("Rphone", phone))
            res = self.rider_sys.multiSearch(keylist)
        elif current_tab == "订单":
            # 执行订单查询操作
            user_address = input_values["配送地址"]
            user_phone = input_values["用户电话"]
            seller_address = input_values["店家地址"]
            seller_phone = input_values["商家电话"]
            rider_name = input_values["骑手姓名"]
            rider_phone = input_values["骑手电话"]
            keylist = []
            if seller_address != '':
                keylist.append(("Saddr", seller_address))
            if seller_phone != '':
                keylist.append(("Sphone", seller_phone))
            if user_address != '':
                keylist.append(("Uaddr", user_address))
            if user_phone != '':
                keylist.append(("Uphone", user_phone))
            if rider_name != '':
                keylist.append(("Rname", rider_name))
            if rider_phone != '':
                keylist.append(("Rphone", rider_phone))
            res = self.order_sys.multiSearch(keylist)
        for item in res:
            current_tree.insert('', 'end', text='', values=item)
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, f"查询到{len(res)}个结果。")
        
    def add(self):
        current_tab = self.tabControl.tab(self.tabControl.select(), "text")  # 获取当前选项卡的文本
        
        input_values = {}
        for field, entry in self.input_fields.items():
            input_values[field] = entry.get()

        print("Input values:", input_values)  # 打印输入的值
        if current_tab == "用户":
            # 执行用户添加操作
            name = input_values["昵称"]
            address = input_values["用户地址"]
            phone = input_values["手机"]
            temp = User(Uname = name, Uaddr = address, Uphone = phone)
            res = self.user_sys.add(temp)
        elif current_tab == "商家":
            # 执行商家添加操作     
            name = input_values["商家名称"]
            address = input_values["商家地址"]
            phone = input_values["电话"]
            temp = Seller(Sname = name, Saddr = address, Sphone = phone)
            res = self.seller_sys.add(temp)
        elif current_tab == "骑手":
            # 执行骑手添加操作
            name = input_values["骑手名称"]
            phone = input_values["联系方式"]
            temp = Rider(Rname = name, Rphone = phone)
            res = self.rider_sys.add(temp)
        elif current_tab == "订单":
            # 执行订单添加操作
        # "配送地址", "用户电话", "店家地址", "商家电话", "骑手姓名", "骑手电话"
            user_address = input_values["配送地址"]
            user_phone = input_values["用户电话"]
            seller_address = input_values["店家地址"]
            seller_phone = input_values["商家电话"]
            rider_name = input_values["骑手姓名"]
            rider_phone = input_values["骑手电话"]
            temp = Order(Saddr = seller_address, 
                         Sphone = seller_phone, 
                         Uaddr = user_address, 
                         Uphone = user_phone, 
                         Rname = rider_name,
                         Rphone = rider_phone)
            res = self.seller_sys.add(temp)   
        if res[0]:
            self.info_text.delete("1.0", tk.END)
            self.info_text.insert(tk.END, "添加成功！")
        else:
            self.info_text.delete("1.0", tk.END)
            self.info_text.insert(tk.END, "添加失败：" + res[1])      
        
    def delete(self):
        current_tab = self.tabControl.tab(self.tabControl.select(), "text")  # 获取当前选项卡的文本
                
        input_values = {}
        for field, entry in self.input_fields.items():
            input_values[field] = entry.get()
        
        if current_tab == "用户":
            # 执行用户删除操作
            user_id = input_values["用户ID"]
            res = self.user_sys.delete(self.user_sys.userUID[user_id])
            if res[0]:
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除成功！")
            else:
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除失败：" + res[1])
            
        elif current_tab == "商家":
            # 执行商家删除操作
            seller_id = input_values["商家ID"]
            res = self.seller_sys.delete(self.seller_sys.sellerSID[seller_id])
            if res[0]:
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除成功！")
            else:
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除失败：" + res[1])
        elif current_tab == "骑手":
            # 执行骑手删除操作
            rider_id = input_values["商家ID"]
            res = self.rider_sys.delete(self.rider_sys.rider_RID[rider_id])
            if res[0]:
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除成功！")
            else:
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除失败：" + res[1])
        elif current_tab == "订单":
            # 执行订单删除操作
            order_id = input_values["商家ID"]
            res = self.order_sys.delete(self.order_sys.order_OID[order_id])
            if res[0]:
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除成功！")
            else:
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert(tk.END, "删除失败：" + res[1])

    def on_tab_changed(self, event):
        # 当选项卡切换时调用此方法
        # 清空输入框内容
        for entry in self.input_fields.values():
            entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = DatabaseUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
