import os
import re
import json
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import winreg
import ctypes
import sys

# =======================================================
# LM Studio换源工具 - Python版
# 功能：图形界面+一键换源+路径浏览
# 作者：Mison
# 邮箱：1360962086@qq.com
# 许可证：MIT
# 打包命令：pyinstaller --onefile --windowed LMStudio_Source_Tool.py
# =======================================================

class LMStudioTool:
    def __init__(self, root):
        self.root = root
        self.root.title("LM Studio 源管理工具 v2.0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 初始化日志
        self.logger = logging.getLogger("LMStudioTool")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # 控制台日志
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        
        # 创建UI
        self.create_widgets()
        
        # 自动检测路径
        self.detect_path()
    
    def create_widgets(self):
        # 顶部标题
        title_frame = tk.Frame(self.root)
        title_frame.pack(pady=10)
        
        tk.Label(title_frame, text="LM Studio 源管理工具", font=("Arial", 16, "bold")).pack()
        tk.Label(title_frame, text="作者: Mison | 邮箱: 1360962086@qq.com | 许可证: MIT").pack(pady=5)
        
        # 路径选择区域
        path_frame = tk.LabelFrame(self.root, text="安装路径设置")
        path_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(path_frame, text="检测到的路径:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.path_var = tk.StringVar()
        tk.Entry(path_frame, textvariable=self.path_var, width=60, state="readonly").grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(path_frame, text="浏览...", command=self.browse_path).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(path_frame, text="重新检测", command=self.detect_path).grid(row=0, column=3, padx=5, pady=5)
        
        # 操作按钮区域
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="一键换源", command=self.smart_replace, 
                 bg="#4CAF50", fg="white", height=2, width=15).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="还原备份", command=self.restore_backup,
                 bg="#2196F3", fg="white", height=2, width=15).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="查看日志", command=self.show_logs,
                 bg="#9E9E9E", fg="white", height=2, width=15).grid(row=0, column=2, padx=10)
        
        # 日志区域
        log_frame = tk.LabelFrame(self.root, text="操作日志")
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10)
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.log_text.config(state="disabled")
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        tk.Label(self.root, textvariable=self.status_var, bd=1, relief="sunken", anchor="w").pack(side="bottom", fill="x")
    
    def log_message(self, message, level="info"):
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"{message}\n")
        self.log_text.config(state="disabled")
        self.log_text.see("end")
        
        if level == "error":
            self.logger.error(message)
        elif level == "warning":
            self.logger.warning(message)
        else:
            self.logger.info(message)
        
        self.status_var.set(message)
        self.root.update()
    
    def detect_path(self):
        """自动检测LM Studio安装路径"""
        self.log_message("开始检测LM Studio安装路径...")
        
        # 1. 检查注册表
        paths = self.check_registry()
        if paths:
            self.path_var.set(paths[0])
            self.log_message(f"从注册表发现安装路径: {paths[0]}")
            return
        
        # 2. 检查常见路径
        common_paths = [
            os.path.join(os.environ['PROGRAMFILES'], 'LM Studio'),
            os.path.join(os.environ['PROGRAMFILES(X86)'], 'LM Studio'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Programs', 'LM Studio'),
            'D:\\Program Files\\LM Studio',
            'E:\\Program Files\\LM Studio'
        ]
        
        for path in common_paths:
            if self.validate_path(path):
                self.path_var.set(path)
                self.log_message(f"在常见路径发现安装: {path}")
                return
        
        self.log_message("无法自动检测到安装路径，请手动浏览", "warning")
    
    def check_registry(self):
        """检查注册表获取安装路径"""
        reg_keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\LM Studio"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\LM Studio"),
        ]
        
        valid_paths = []
        
        for hive, key_path in reg_keys:
            try:
                key = winreg.OpenKey(hive, key_path)
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    
                    try:
                        # 尝试获取安装路径
                        path = None
                        try:
                            path, _ = winreg.QueryValueEx(subkey, "InstallLocation")
                        except:
                            pass
                        
                        if not path:
                            try:
                                path, _ = winreg.QueryValueEx(subkey, "InstallPath")
                            except:
                                pass
                        
                        # 验证路径
                        if path and self.validate_path(path):
                            valid_paths.append(path)
                    finally:
                        winreg.CloseKey(subkey)
            except:
                pass
        
        return valid_paths
    
    def validate_path(self, path):
        """验证路径是否有效"""
        target_file = os.path.join(path, 'resources', 'app', '.webpack', 'renderer', 'main_window.js')
        return os.path.exists(target_file)
    
    def browse_path(self):
        """浏览文件夹选择安装路径"""
        path = filedialog.askdirectory(title="选择LM Studio安装目录")
        if path:
            if self.validate_path(path):
                self.path_var.set(path)
                self.log_message(f"已选择安装路径: {path}")
            else:
                messagebox.showerror("错误", "选择的路径无效，未找到LM Studio文件")
    
    def smart_replace(self):
        """一键换源操作"""
        path = self.path_var.get()
        if not path or not self.validate_path(path):
            messagebox.showerror("错误", "请先选择有效的LM Studio安装路径")
            return
        
        if not self.is_admin():
            messagebox.showinfo("提示", "需要管理员权限，请重新运行程序")
            return
        
        # 执行换源操作
        files = [
            os.path.join(path, 'resources', 'app', '.webpack', 'renderer', 'main_window.js'),
            os.path.join(path, 'resources', 'app', '.webpack', 'main', 'index.js')
        ]
        
        success = True
        for file_path in files:
            if not os.path.exists(file_path):
                self.log_message(f"文件不存在: {file_path}", "error")
                success = False
                continue
            
            try:
                # 创建备份
                backup_path = file_path + '.bak'
                if not os.path.exists(backup_path):
                    import shutil
                    shutil.copy2(file_path, backup_path)
                    self.log_message(f"已创建备份: {backup_path}")
                
                # 读取并替换内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                updated = re.sub(r'huggingface\.co', 'hf-mirror.com', content)
                
                if content == updated:
                    self.log_message(f"无需更改: {file_path}", "warning")
                else:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated)
                    self.log_message(f"已替换: {file_path}")
                    
                    # 验证
                    with open(file_path, 'r', encoding='utf-8') as f:
                        new_content = f.read()
                    
                    if 'hf-mirror.com' in new_content:
                        self.log_message("验证成功: 替换内容已确认")
                    else:
                        self.log_message("验证失败: 未检测到替换内容", "warning")
            except Exception as e:
                self.log_message(f"处理失败: {file_path} - {str(e)}", "error")
                success = False
        
        if success:
            messagebox.showinfo("完成", "换源操作成功完成！")
        else:
            messagebox.showwarning("完成", "换源操作完成，但部分文件处理失败，请查看日志")
    
    def restore_backup(self):
        """还原备份"""
        path = self.path_var.get()
        if not path or not self.validate_path(path):
            messagebox.showerror("错误", "请先选择有效的LM Studio安装路径")
            return
        
        if not self.is_admin():
            messagebox.showinfo("提示", "需要管理员权限，请重新运行程序")
            return
        
        # 执行还原操作
        files = [
            os.path.join(path, 'resources', 'app', '.webpack', 'renderer', 'main_window.js'),
            os.path.join(path, 'resources', 'app', '.webpack', 'main', 'index.js')
        ]
        
        success = True
        for file_path in files:
            backup_path = file_path + '.bak'
            if not os.path.exists(backup_path):
                self.log_message(f"备份不存在: {backup_path}", "warning")
                continue
            
            try:
                import shutil
                shutil.copy2(backup_path, file_path)
                self.log_message(f"已从备份恢复: {file_path}")
                
                os.remove(backup_path)
                self.log_message(f"已删除备份: {backup_path}")
            except Exception as e:
                self.log_message(f"还原失败: {file_path} - {str(e)}", "error")
                success = False
        
        if success:
            messagebox.showinfo("完成", "还原操作成功完成！")
        else:
            messagebox.showwarning("完成", "还原操作完成，但部分文件处理失败，请查看日志")
    
    def show_logs(self):
        """显示日志窗口（已集成在主界面）"""
        self.log_text.see("end")
    
    def is_admin(self):
        """检查管理员权限"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

if __name__ == "__main__":
    # 请求管理员权限
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()
    
    root = tk.Tk()
    app = LMStudioTool(root)
    root.mainloop()