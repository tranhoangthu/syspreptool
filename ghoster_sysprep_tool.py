import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import threading
import os
import getpass

# Đường dẫn WinPE mặc định
WINPE_WIM_PATH = os.path.abspath('winpe/W11x64.wim')
UNATTEND_PATH = os.path.abspath('unattend.xml')

UNATTEND_XML = '''<?xml version="1.0" encoding="utf-8"?>
<unattend xmlns="urn:schemas-microsoft-com:unattend">
  <settings pass="specialize">
    <component name="Microsoft-Windows-Shell-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" xmlns:wcm="http://schemas.microsoft.com/WMIConfig/2002/State" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <CopyProfile>true</CopyProfile>
    </component>
  </settings>
</unattend>
'''

class GhosterSysprepTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('SYSPREP TOOL HOANGTHUIT 2025 V1.2')
        self.geometry('650x430')
        self.resizable(False, False)
        self.driver_path = tk.StringVar()
        self.status = tk.StringVar(value='Ready.')
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Segoe UI', 10))
        self.style.configure('TLabel', font=('Segoe UI', 10))
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Tab SYSPREP
        sysprep_tab = ttk.Frame(notebook)
        notebook.add(sysprep_tab, text='SYSPREP')
        # Add Drivers
        driver_frame = ttk.LabelFrame(sysprep_tab, text='Thêm Driver Cho Windows (Ví dụ: Driver Ổ Cứng Cho Máy CPU Gen 10/11/12/13/14)')
        driver_frame.pack(fill='x', padx=10, pady=10)
        ttk.Entry(driver_frame, textvariable=self.driver_path, width=66).pack(side='left', padx=5, pady=5)
        ttk.Button(driver_frame, text='Browse', command=self.browse_driver).pack(side='left', padx=5)
        ttk.Button(driver_frame, text='SYSPREP', command=self.start_sysprep).pack(side='left', padx=5)

        # Hướng dẫn
        guide = (
            'Quy trình hoạt động:\n'
            '1. Sau khi cài đặt phần mềm, tinh chỉnh cá nhân hoá Windows,\n'
            '   chọn Browse để Add thêm Drivers cho bản Ghost nếu muốn.\n'
            '2. Click SYSPREP, tool sẽ tự động tạo file unattend.xml với CopyProfile=true,\n'
            '   chạy Sysprep với answer file này để giữ lại mọi tinh chỉnh cho user mới.\n'
            '3. Sau khi Sysprep, máy sẽ khởi động lại và boot vào WinPE, có các công cụ backup.\n'
            '4. Sau khi bung ghost, Windows sẽ tạo 1 user mới hoàn toàn với mọi tinh chỉnh đã lưu.\n'
        )
        guide_label = ttk.Label(sysprep_tab, text=guide, anchor='w', justify='left')
        guide_label.pack(fill='x', padx=10, pady=5)

        # Khung log
        log_frame = ttk.LabelFrame(sysprep_tab, text='Log')
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        log_text = tk.Text(log_frame, bg='black', fg='green', font=('Consolas', 10), wrap='word')
        log_text.pack(fill='both', expand=True, padx=5, pady=5)
        log_text.tag_configure('log', foreground='green')
        log_text.insert('end', self.status.get(), 'log')
        log_text.config(state='disabled')
        self.log_text = log_text

        # Thanh trạng thái
        status_frame = ttk.Frame(sysprep_tab)
        status_frame.pack(side='bottom', fill='x', pady=5)
        ttk.Label(status_frame, text='Trạng Thái:').pack(side='left', padx=5)
        ttk.Label(status_frame, textvariable=self.status, foreground='green').pack(side='left')

        # Tab About
        about_tab = ttk.Frame(notebook)
        notebook.add(about_tab, text='ABOUT')
        about_frame = ttk.Frame(about_tab)
        about_frame.pack(fill='both', expand=True, padx=10, pady=10)
        about_text = (
            'SYSPREP TOOL V1.2 2025\n'
            'Tác giả: HoangThuIT\n'
            'Website: https://hoangthu.liveblog365.com\n'
            '\n'
            'Công cụ tự động Sysprep, giữ lại mọi tinh chỉnh,\n'
            'tích hợp boot WinPE và backup ghost.\n'
            '\n'
            'Hỗ trợ: Windows 10/11 (win 7 lỗi win 8 chưa test)\n'
            'Liên hệ hỗ trợ: fb.com/tranhoangthuit\n'
        )
        ttk.Label(about_frame, text=about_text, anchor='w', justify='left', font=('Segoe UI', 11, 'bold')).pack(side='left', fill='both', expand=True)
        # Hiển thị hình ảnh sysprep.svg
        try:
            image = tk.PhotoImage(file='sysprep.png')
            image_label = ttk.Label(about_frame, image=image)
            image_label.image = image  # Giữ tham chiếu để tránh garbage collection
            image_label.pack(side='right', fill='both', expand=True)
        except Exception as e:
            ttk.Label(about_frame, text='[Không thể tải hình ảnh]', anchor='center', font=('Segoe UI', 11, 'bold')).pack(side='right', fill='both', expand=True)

        # Tab Settings
        settings_tab = ttk.Frame(notebook)
        notebook.add(settings_tab, text='SETTINGS')
        theme_frame = ttk.LabelFrame(settings_tab, text='Theme')
        theme_frame.pack(fill='x', padx=10, pady=10)
        ttk.Label(theme_frame, text='Chọn theme:').pack(side='left', padx=5)
        theme_combo = ttk.Combobox(theme_frame, values=['clam', 'alt', 'default', 'classic'], state='readonly')
        theme_combo.set('clam')
        theme_combo.pack(side='left', padx=5)
        theme_combo.bind('<<ComboboxSelected>>', self.change_theme)

        # Tùy chọn sau khi Sysprep
        sysprep_frame = ttk.LabelFrame(settings_tab, text='Sau khi Sysprep')
        sysprep_frame.pack(fill='x', padx=10, pady=10)
        self.sysprep_action = tk.StringVar(value='restart')
        ttk.Radiobutton(sysprep_frame, text='Tắt Máy', variable=self.sysprep_action, value='shutdown').pack(anchor='w', padx=5, pady=2)
        ttk.Radiobutton(sysprep_frame, text='Khởi Động Lại và Boot vào WinPE', variable=self.sysprep_action, value='restart').pack(anchor='w', padx=5, pady=2)
        ttk.Radiobutton(sysprep_frame, text='Không Làm Gì', variable=self.sysprep_action, value='none').pack(anchor='w', padx=5, pady=2)

    def change_theme(self, event):
        theme = event.widget.get()
        self.style.theme_use(theme)

    def browse_driver(self):
        path = filedialog.askopenfilename(title='Chọn file driver hoặc thư mục driver')
        if path:
            self.driver_path.set(path)

    def start_sysprep(self):
        t = threading.Thread(target=self.sysprep_process)
        t.start()

    def sysprep_process(self):
        self.status.set('Đang xử lý...')
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert('end', 'Đang xử lý...\n', 'log')
        self.log_text.config(state='disabled')
        progress = ttk.Progressbar(self, orient='horizontal', length=300, mode='determinate')
        progress.pack(side='bottom', fill='x', padx=10, pady=5)
        progress['value'] = 0
        try:
            # 1. Tự động tạo unattend.xml với CopyProfile=true
            self.status.set('Đang tạo file unattend.xml...')
            self.log_text.config(state='normal')
            self.log_text.insert('end', 'Đang tạo file unattend.xml...\n', 'log')
            self.log_text.config(state='disabled')
            with open(UNATTEND_PATH, 'w', encoding='utf-8') as f:
                f.write(UNATTEND_XML)
            progress['value'] = 20
            # 2. Thêm driver nếu có
            driver = self.driver_path.get()
            if driver:
                self.status.set('Đang thêm driver...')
                self.log_text.config(state='normal')
                self.log_text.insert('end', 'Đang thêm driver...\n', 'log')
                self.log_text.config(state='disabled')
                subprocess.run(f'pnputil /add-driver "{driver}" /install', shell=True, check=True)
            progress['value'] = 40
            # 3. Chạy Sysprep với answer file (KHÔNG tắt máy)
            self.status.set('Đang chạy Sysprep...')
            self.log_text.config(state='normal')
            self.log_text.insert('end', 'Đang chạy Sysprep...\n', 'log')
            self.log_text.config(state='disabled')
            sysprep_cmd = fr'C:\Windows\System32\Sysprep\sysprep.exe /generalize /oobe /quit /unattend:"{UNATTEND_PATH}"'
            subprocess.run(sysprep_cmd, shell=True, check=True)
            progress['value'] = 60
            self.status.set('Sysprep hoàn tất! Tiếp tục thiết lập boot vào WinPE...')
            self.log_text.config(state='normal')
            self.log_text.insert('end', 'Sysprep hoàn tất! Tiếp tục thiết lập boot vào WinPE...\n', 'log')
            self.log_text.config(state='disabled')
            # 4. Thiết lập boot vào WinPE bằng script
            script_path = os.path.abspath('winpe/1Click-Win11x64.cmd')
            try:
                subprocess.run(f'"{script_path}"', shell=True, check=True, cwd=os.path.dirname(script_path), capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                self.status.set(f'Lỗi: {e}\n{e.stdout}\n{e.stderr}')
                self.log_text.config(state='normal')
                self.log_text.insert('end', f'Lỗi: {e}\n{e.stdout}\n{e.stderr}\n', 'log')
                self.log_text.config(state='disabled')
                return
            progress['value'] = 80
            self.status.set('Hoàn thành! Máy sẽ khởi động lại vào WinPE để backup.')
            self.log_text.config(state='normal')
            self.log_text.insert('end', 'Hoàn thành! Máy sẽ khởi động lại vào WinPE để backup.\n', 'log')
            self.log_text.config(state='disabled')
            # 5. Xử lý hành động sau khi Sysprep
            action = self.sysprep_action.get()
            if action == 'shutdown':
                # Hiện cửa sổ mới có text chạy đếm ngược
                countdown_window = tk.Toplevel(self)
                countdown_window.title('Thông báo')
                countdown_window.geometry('300x100')
                countdown_label = ttk.Label(countdown_window, text='Còn 10 giây nữa máy sẽ Tắt Máy', font=('Segoe UI', 11, 'bold'))
                countdown_label.pack(expand=True)
                def update_countdown(count):
                    if count > 0:
                        countdown_label.config(text=f'Còn {count} giây nữa máy sẽ Tắt Máy')
                        countdown_window.after(1000, update_countdown, count - 1)
                    else:
                        countdown_window.destroy()
                update_countdown(10)
            elif action == 'restart':
                # Hiện cửa sổ mới có text chạy đếm ngược
                countdown_window = tk.Toplevel(self)
                countdown_window.title('Thông báo')
                countdown_window.geometry('300x100')
                countdown_label = ttk.Label(countdown_window, text='Còn 10 giây nữa máy sẽ Khởi Động Lại Vào WinPE', font=('Segoe UI', 11, 'bold'))
                countdown_label.pack(expand=True)
                def update_countdown(count):
                    if count > 0:
                        countdown_label.config(text=f'Còn {count} giây nữa máy sẽ Khởi Động Lại Vào WinPE')
                        countdown_window.after(1000, update_countdown, count - 1)
                    else:
                        countdown_window.destroy()
                        # Chạy lệnh cmd boot vào winpe
                        script_path = os.path.abspath('winpe/boot.cmd')
                        subprocess.run(f'"{script_path}"', shell=True, check=True, cwd=os.path.dirname(script_path), capture_output=True, text=True)
                update_countdown(10)
            # Nếu action là 'none', không làm gì
            progress['value'] = 100
        except Exception as e:
            self.status.set(f'Lỗi: {e}')
            self.log_text.config(state='normal')
            self.log_text.insert('end', f'Lỗi: {e}\n', 'log')
            self.log_text.config(state='disabled')

if __name__ == '__main__':
    app = GhosterSysprepTool()
    app.mainloop()
