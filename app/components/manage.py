import tkinter as tk
import json
import os

class ManageComponent:
    def __init__(self, master):
        self.top_frame = tk.Frame(master)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.listbox = tk.Listbox(self.top_frame, bg='white')
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = tk.Scrollbar(self.top_frame, orient="vertical")
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        
        self.selected_file = None
        self.batch_files = []
        
        self.load_batch_files()

    def on_select(self, event):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            self.selected_file = self.listbox.get(index)
            print(f"選択されたファイル: {self.selected_file}")

    def get_selected_file(self):
        return self.selected_file

    def add_batch_file(self, filename):
        if filename and filename not in self.batch_files:
            self.batch_files.append(filename)
            self.listbox.insert(tk.END, filename)
            self.save_batch_files()
            
    def delete_selected_file(self):
        if self.selected_file:
            index = self.listbox.get(0, tk.END).index(self.selected_file)
            self.listbox.delete(index)
            self.batch_files.remove(self.selected_file)
            self.selected_file = None
            self.save_batch_files()
            print(f"ファイルを削除しました: {self.selected_file}")

    def save_batch_files(self):
        with open('batch_files.json', 'w') as f:
            json.dump(self.batch_files, f)

    def load_batch_files(self):
        if os.path.exists('batch_files.json'):
            with open('batch_files.json', 'r') as f:
                self.batch_files = json.load(f)
            for file in self.batch_files:
                self.listbox.insert(tk.END, file)