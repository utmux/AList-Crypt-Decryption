import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import subprocess
import threading
import os

class CryptoGUI(tk.Tk):
    """一个用于 crypto_tool.py 的图形化前端界面"""

    def __init__(self):
        super().__init__()
        self.title("AList Crypt 加解密工具")
        self.geometry("700x650")

        # 让窗口大小可调整
        self.columnconfigure(1, weight=1)

        # -- 定义 Tkinter 变量 --
        self.action_var = tk.StringVar(value="encrypt")
        self.input_path_var = tk.StringVar()
        self.output_path_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.salt_var = tk.StringVar()
        self.filename_enc_var = tk.StringVar(value="off")
        self.directory_enc_var = tk.BooleanVar(value=False)
        self.suffix_var = tk.StringVar(value=".bin")
        self.filename_enc_mode_var = tk.StringVar(value="base64")

        # -- 创建控件 --
        self._create_widgets()

    def _create_widgets(self):
        """创建界面上的所有控件"""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # -- 参数配置区 --
        options_frame = ttk.LabelFrame(main_frame, text="配置参数", padding="10")
        options_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=5)
        options_frame.columnconfigure(1, weight=1)

        # 动作: 加密/解密
        ttk.Label(options_frame, text="操作类型:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        action_subframe = ttk.Frame(options_frame)
        action_subframe.grid(row=0, column=1, columnspan=2, sticky="w")
        ttk.Radiobutton(action_subframe, text="加密", variable=self.action_var, value="encrypt").pack(side="left", padx=5)
        ttk.Radiobutton(action_subframe, text="解密", variable=self.action_var, value="decrypt").pack(side="left", padx=5)

        # 路径选择
        self._create_path_entry(options_frame, "输入目录:", self.input_path_var, 1)
        self._create_path_entry(options_frame, "输出目录:", self.output_path_var, 2)
        
        # 密码和盐值
        ttk.Label(options_frame, text="密码:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(options_frame, textvariable=self.password_var, show="*").grid(row=3, column=1, sticky="ew")
        
        ttk.Label(options_frame, text="盐值 (可选):").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(options_frame, textvariable=self.salt_var, show="*").grid(row=4, column=1, sticky="ew")

        # 高级选项
        ttk.Label(options_frame, text="文件名加密:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        ttk.Combobox(options_frame, textvariable=self.filename_enc_var, values=["off", "standard", "obfuscate"], state="readonly").grid(row=5, column=1, sticky="ew")
        
        ttk.Label(options_frame, text="目录名加密:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        ttk.Checkbutton(options_frame, variable=self.directory_enc_var, onvalue=True, offvalue=False).grid(row=6, column=1, sticky="w")

        ttk.Label(options_frame, text="加密后缀:").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(options_frame, textvariable=self.suffix_var).grid(row=7, column=1, sticky="ew")

        ttk.Label(options_frame, text="文件名编码:").grid(row=8, column=0, sticky="w", padx=5, pady=5)
        ttk.Combobox(options_frame, textvariable=self.filename_enc_mode_var, values=["base64", "base32", "base32768"], state="readonly").grid(row=8, column=1, sticky="ew")

        # -- 执行按钮 --
        self.run_button = ttk.Button(main_frame, text="开始执行", command=self.start_process)
        self.run_button.grid(row=1, column=0, columnspan=3, pady=10)

        # -- 输出日志区 --
        output_frame = ttk.LabelFrame(main_frame, text="执行日志", padding="10")
        output_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")
        main_frame.rowconfigure(2, weight=1)
        output_frame.rowconfigure(0, weight=1)
        output_frame.columnconfigure(0, weight=1)

        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, state="disabled")
        self.output_text.grid(row=0, column=0, sticky="nsew")
        
    def _create_path_entry(self, parent, label_text, var, row):
        """创建一个带'浏览'按钮的路径输入框"""
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(parent, textvariable=var).grid(row=row, column=1, sticky="ew")
        ttk.Button(parent, text="浏览...", command=lambda: self._browse_directory(var)).grid(row=row, column=2, padx=5)

    def _browse_directory(self, path_var):
        """打开目录选择对话框"""
        directory = filedialog.askdirectory()
        if directory:
            path_var.set(directory)

    def start_process(self):
        """开始执行 crypto_tool.py 脚本"""
        # 1. 验证输入
        if not self.input_path_var.get() or not self.output_path_var.get():
            messagebox.showerror("错误", "输入和输出目录不能为空！")
            return
        if not self.password_var.get():
            messagebox.showerror("错误", "密码不能为空！")
            return
        
        # 2. 构建命令
        command = self._build_command()
        
        # 3. 在新线程中执行命令，防止GUI卡死
        self.run_button.config(state="disabled")
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"即将执行命令:\n{' '.join(command)}\n\n")
        self.output_text.config(state="disabled")

        thread = threading.Thread(target=self._run_command_in_thread, args=(command,))
        thread.daemon = True
        thread.start()

    def _build_command(self) -> list:
        """根据GUI输入构建命令行参数列表"""
        script_path = os.path.join(os.path.dirname(__file__), "crypto_tool.py")
        command = [
            "python", script_path,
            self.action_var.get(),
            "--input", self.input_path_var.get(),
            "--output", self.output_path_var.get(),
            "--password", self.password_var.get(),
        ]
        if self.salt_var.get():
            command.extend(["--salt", self.salt_var.get()])
        
        command.extend(["--filename-encryption", self.filename_enc_var.get()])
        
        if self.directory_enc_var.get():
            command.append("--directory-encryption")
            
        command.extend(["--suffix", self.suffix_var.get()])
        command.extend(["--filename-encoding", self.filename_enc_mode_var.get()])
        
        return command

    def _run_command_in_thread(self, command):
        """在子线程中运行命令并实时更新GUI"""
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                bufsize=1, # 行缓冲
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0 # Windows下不显示控制台窗口
            )

            # 实时读取输出
            for line in iter(process.stdout.readline, ''):
                self.after(0, self._append_output, line)

            process.stdout.close()
            return_code = process.wait()
            
            if return_code == 0:
                self.after(0, self._append_output, "\n--- 操作成功完成！ ---")
            else:
                self.after(0, self._append_output, f"\n--- 操作失败，返回码: {return_code} ---")

        except FileNotFoundError:
             self.after(0, self._append_output, f"\n错误: 找不到脚本 'crypto_tool.py'。请确保它和GUI程序在同一个目录下。")
        except Exception as e:
            self.after(0, self._append_output, f"\n执行时发生未知错误: {e}")
        finally:
            self.after(0, self.run_button.config, {"state": "normal"}) # 任务结束后恢复按钮

    def _append_output(self, text):
        """安全地从子线程向GUI文本框追加内容"""
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END) # 自动滚动到底部
        self.output_text.config(state="disabled")

if __name__ == "__main__":
    app = CryptoGUI()
    app.mainloop()