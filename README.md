# SYSPREP TOOL HOANGTHUIT 2025 V1.2

## Mô tả
SYSPREP TOOL là công cụ tự động hóa quá trình Sysprep, giúp giữ lại mọi tinh chỉnh cá nhân hóa Windows, tích hợp boot WinPE và backup ghost. Tool hỗ trợ Windows 10/11, với giao diện thân thiện, dễ sử dụng.

![SYSPREP TOOL](sysprep.png)
## Tính năng
- Tự động tạo file unattend.xml với CopyProfile=true, giữ lại mọi tinh chỉnh cho user mới.
- Thêm driver cho Windows (ví dụ: Driver ổ cứng cho máy CPU Gen 10/11/12/13/14).
- Chạy Sysprep với answer file, không tắt máy.
- Thiết lập boot vào WinPE bằng script.
- Hiển thị tiến trình chạy trong log, không hiện thông báo.
- Tùy chọn hành động sau khi Sysprep: Tắt Máy, Khởi Động Lại và Boot vào WinPE, hoặc Không Làm Gì.
- Giao diện hiện đại với ttk, hỗ trợ đổi theme.

## Hướng dẫn sử dụng
1. **Cài đặt phần mềm và tinh chỉnh cá nhân hóa Windows**:
   - Cài đặt các phần mềm cần thiết.
   - Tinh chỉnh cá nhân hóa Windows theo ý muốn.

2. **Thêm Driver (tùy chọn)**:
   - Chọn Browse để thêm driver cho bản Ghost nếu muốn.
   - Ví dụ: Driver ổ cứng cho máy CPU Gen 10/11/12/13/14.

3. **Chạy Sysprep**:
   - Click SYSPREP, tool sẽ tự động tạo file unattend.xml với CopyProfile=true.
   - Chạy Sysprep với answer file này để giữ lại mọi tinh chỉnh cho user mới.

4. **Thiết lập boot vào WinPE**:
   - Sau khi Sysprep, máy sẽ khởi động lại và boot vào WinPE.
   - Có các công cụ backup trong WinPE.

5. **Tùy chọn sau khi Sysprep**:
   - Tắt Máy: Hiện bảng thông báo đếm ngược, sau đó tắt máy.
   - Khởi Động Lại và Boot vào WinPE: Hiện bảng thông báo đếm ngược, sau đó chạy lệnh cmd boot vào winpe.
   - Không Làm Gì: Không thực hiện hành động nào.

6. **Đổi theme (tùy chọn)**:
   - Vào tab Settings, chọn theme từ danh sách có sẵn.

## Hướng dẫn tùy chỉnh (Nếu rành về code)
### 1. Chỉnh sửa giao diện hoặc chức năng
- Mở file `ghoster_sysprep_tool.py` bằng trình soạn thảo code (VSCode, Notepad++, ...).
- Sửa các hàm, giao diện, text, hoặc thêm tab mới theo ý muốn.
- Có thể chỉnh sửa các bước Sysprep, log, theme, hoặc thêm chức năng mới.

### 2. Thay đổi script boot WinPE
- Thay đổi đường dẫn hoặc nội dung file `winpe/boot.cmd` theo ý muốn.
- Đảm bảo file script và file WinPE (`winpe.wim`) nằm đúng vị trí thư mục `winpe`.

### 3. Thay đổi icon ứng dụng
- Thay file `sysprep.png` bằng icon mới (cùng tên hoặc sửa lại đường dẫn trong code).
- Khi build exe, có thể dùng file `.ico` với PyInstaller: `--icon=sysprep.ico`.

### 4. Build lại file exe
- Cài Python 3.x và pip nếu chưa có.
- Cài PyInstaller: `pip install pyinstaller`
- Build:
  
  ```
  pyinstaller --onefile --windowed --icon=sysprep.ico --name="SYSPREP TOOL HOANGTHUIT 2025 V1.2" ghoster_sysprep_tool.py
  ```
- File exe sẽ nằm trong thư mục `dist`. Copy kèm thư mục `winpe`.

### 5. Thêm/tùy chỉnh driver
- Có thể thay đổi logic thêm driver trong hàm `sysprep_process`.
- Hỗ trợ cả file `.inf` hoặc thư mục chứa nhiều driver.

### 6. Đổi theme mặc định
- Sửa dòng `self.style.theme_use('clam')` trong hàm `__init__` thành theme bạn muốn.

## Lưu ý
- Tool hỗ trợ Windows 10/11 (Windows 7 có thể sử dụng nhưng không giữ lại các tinh chỉnh) (Windows 8 Chưa Test).
- Khi chạy file exe trên máy khác, cần đảm bảo:
  - Copy cả thư mục `winpe` chứa file `boot.cmd` và `winpe.wim`.
  - File exe và thư mục `winpe` phải nằm cùng thư mục.
  - Chạy file exe với quyền Administrator.
  - Thư mục tool và driver không được đặt vào Ổ C nên để ở các ổ như D,E,F,... 

## Liên hệ hỗ trợ
- Tác giả: HoangThuIT
- Website: https://hoangthu.liveblog365.com
- Facebook: fb.com/tranhoangthuit
