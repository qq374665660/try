# main.py
import tkinter as tk
from ttkbootstrap import Style
import sqlite3

class ResearchManager:
    def __init__(self):
        self.window = tk.Tk()
        self.style = Style(theme='minty')
        self.window.title("科研课题管理系统")
        
        # 连接数据库
        self.conn = sqlite3.connect('projects.db')
        self.create_table()
        
        # 创建主界面
        self.create_widgets()
        self.load_projects()
        
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS projects
                          (id INTEGER PRIMARY KEY, 
                           name TEXT, 
                           progress INTEGER, 
                           leader TEXT)''')
        self.conn.commit()
    
    def create_widgets(self):
        # 课题列表
        self.tree = tk.ttk.Treeview(self.window, columns=('name', 'progress', 'leader'), show='headings')
        self.tree.heading('name', text='课题名称')
        self.tree.heading('progress', text='进度 (%)')
        self.tree.heading('leader', text='负责人')
        self.tree.pack(fill='both', expand=True)
        
        # 添加课题按钮
        add_btn = tk.Button(self.window, text="新增课题", command=self.add_project)
        add_btn.pack(side='left')
        
    def load_projects(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, progress, leader FROM projects")
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)
    
    def add_project(self):
        # 简化的添加窗口
        new_window = tk.Toplevel()
        tk.Label(new_window, text="课题名称:").grid(row=0, column=0)
        name_entry = tk.Entry(new_window)
        name_entry.grid(row=0, column=1)
        
        # 保存到数据库
        def save():
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO projects (name, progress, leader) VALUES (?, 0, '待分配')",
                           (name_entry.get(),))
            self.conn.commit()
            self.tree.insert('', 'end', values=(name_entry.get(), 0, '待分配'))
            new_window.destroy()
        
        tk.Button(new_window, text="保存", command=save).grid(row=1, columnspan=2)

if __name__ == "__main__":
    app = ResearchManager()
    app.window.mainloop()