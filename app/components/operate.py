import tkinter as tk
from ..utils.operate_util import OperateUtil
import sys
import io

class OperateComponent:
    def __init__(self, master, manage_component):
        self.master = master
        self.manage_component = manage_component
        self.operate_util = OperateUtil()
        self.bottom_frame = tk.Frame(master)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)

        self.left_frame_setting()
        
        self.right_frame_setting()
        
        self.redirect_stdout()

    def add_batch_file(self):
        filename = self.operate_util.add_batch_file()
        if filename:
            self.manage_component.add_batch_file(filename)
            
    def delete_selected_file(self):
        self.manage_component.delete_selected_file()
        
    def left_frame_setting(self):
        self.bottom_left_frame = tk.Frame(self.bottom_frame, width=500)
        self.bottom_left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        log_label = tk.Label(self.bottom_left_frame, text="実行ログ", font=("Helvetica", 10, "bold"), anchor='w')
        log_label.pack(side=tk.TOP, pady=(2, 0), padx=(10, 0), fill=tk.X)

        text_frame = tk.Frame(self.bottom_left_frame)
        text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(text_frame, wrap=tk.WORD, bg='white', fg='black')
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)

        self.log_text.config(state=tk.DISABLED)
        
    def right_frame_setting(self):
        self.bottom_right_frame = tk.Frame(self.bottom_frame, width=400, borderwidth=2, relief=tk.SUNKEN)
        self.bottom_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        log_label = tk.Label(self.bottom_right_frame, text="操作", font=("Helvetica", 10, "bold"), anchor='w')
        log_label.pack(side=tk.TOP, pady=(2, 0), padx=(10, 0), fill=tk.X)

        button_width = 20
        button_height = 2

        self.add_button = tk.Button(self.bottom_right_frame, text="バッチファイル追加", command=self.add_batch_file, width=button_width, height=button_height)
        self.add_button.pack(side=tk.TOP, pady=10)
    
        self.execute_button = tk.Button(self.bottom_right_frame, text="バッチファイル実行", command=self.execute_batch_file, width=button_width, height=button_height)
        self.execute_button.pack(side=tk.TOP, pady=10)
    
        self.delete_button = tk.Button(self.bottom_right_frame, text="選択ファイルを削除", command=self.delete_selected_file, width=button_width, height=button_height)
        self.delete_button.pack(side=tk.TOP, pady=10)

    def execute_batch_file(self):
        batch_file = self.manage_component.get_selected_file()
        if batch_file:
            self.operate_util.execute_batch_file(batch_file, self.log_text, self.master)
        else:
            print("バッチファイルが選択されていません。")
            
    def redirect_stdout(self):
        class StdoutRedirector(io.StringIO):
            def __init__(self, text_widget):
                self.text_widget = text_widget
                io.StringIO.__init__(self)

            def write(self, string):
                self.text_widget.config(state=tk.NORMAL)
                self.text_widget.insert(tk.END, string)
                self.text_widget.see(tk.END)
                self.text_widget.config(state=tk.DISABLED)

        sys.stdout = StdoutRedirector(self.log_text)
        
