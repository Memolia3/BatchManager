import tkinter as tk
from ..components.manage import ManageComponent
from ..components.operate import OperateComponent

class BatchManagerGUI:
    def __init__(self, master):
        self.master = master
        master.title("バッチマネージャー / BatchManager")
        master.geometry("800x600")

        top_frame = tk.Frame(master)
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        bottom_frame = tk.Frame(master, height=240)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=False)
        bottom_frame.pack_propagate(False)

        self.manage_component = ManageComponent(top_frame)
        self.operate_component = OperateComponent(bottom_frame, self.manage_component)
            
""" run """  
def run():
    root = tk.Tk()
    app = BatchManagerGUI(root)
    root.mainloop()

