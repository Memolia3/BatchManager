from tkinter import filedialog
import tkinter as tk
import subprocess
import threading
import queue
import os
import time

""" operation utility """
class OperateUtil:
    
    """ add batch file """
    @staticmethod
    def add_batch_file():
        return filedialog.askopenfilename(filetypes=[("Batch files", "*.bat")])
    
    """ execute batch file """
    @staticmethod
    def execute_batch_file(batch_file, log_text, root):
        # バッチファイルのディレクトリに移動
        directory = os.path.dirname(batch_file)
        os.chdir(directory)
        
        # ログ出力用関数
        def safe_log(text):
            root.after(0, lambda: log_to_text(text))

        def log_to_text(text):
            log_text.config(state=tk.NORMAL)
            if text is not None:
                if not isinstance(text, str):
                    text = str(text)
                log_text.insert(tk.END, text)
            log_text.see(tk.END)
            log_text.config(state=tk.DISABLED)

        safe_log(f"実行中: {batch_file}\n")

        # 標準出力とエラー出力をキューに書き込む関数
        def read_output(pipe, q):
            try:
                for line in iter(pipe.readline, ''):
                    q.put(line.strip() + '\n')
            finally:
                q.put(None)

        # キューを処理する関数
        def process_queue(q, process):
            try:
                while not q.empty():
                    line = q.get_nowait()
                    if line is None: 
                        return False
                    safe_log(line)
            except queue.Empty:
                pass
            
            if process.poll() is None:
                root.after(100, lambda: process_queue(q, process))
            else:
                safe_log("\nプロセスが終了しました。\n")
                return True

        try:
            # サブプロセスを開始
            process = subprocess.Popen(
                batch_file,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )

            q_stdout = queue.Queue()
            q_stderr = queue.Queue()

            # 標準出力とエラー出力を別スレッドで読み取る
            threading.Thread(target=read_output, args=(process.stdout, q_stdout), daemon=True).start()
            threading.Thread(target=read_output, args=(process.stderr, q_stderr), daemon=True).start()

            # キュー処理を開始
            root.after(100, lambda: process_queue(q_stdout, process))
            root.after(100, lambda: process_queue(q_stderr, process))

        except Exception as e:
            safe_log(f"エラー発生: {str(e)}\n")