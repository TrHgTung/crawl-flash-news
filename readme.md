<h1>TRÌNH TỰ CÁC BƯỚC HƯỚNG DẪN:</h1>

<h2>1/ Trên môi trường test:</h2>
- Clone source code về máy <br>
- Cài python và add python vào biến môi trường: https://www.python.org/downloads/ <br>
- Kiểm tra đã cài python trong máy chưa: Mở Command Prompt -> Nhập `python --version` -> Enter -> nếu hiện version thì cài ok <br>
- Truy cập tới folder source code: Trong Command Prompt nhập `cd /crawl-flash-news/` -> Enter <br>
- Cài môi trường ảo (venv) cho source: trong command prômpt nhập `python -m venv venv` -> Enter <br>
- Bật venv: Trong command prompt nhập `cd \venv\Scripts\` -> Enter -> nhập `activate` -> Enter <br>
- Back ra ngoài source : Trong command prompt nhập `cd ../..` -> Enter <br>
- Cài các thư viện cần thiết: Trong command prompt nhập `pip install -r requirements.txt` -> Enter rồi đợi một lúc <br>
- Chạy thử và kiểm tra: trong command prompt nhập `python app.py` -> Enter rồi đợi. Sau đó kiểm tra dữ liệu đã xuất ra trong tệp: https://docs.google.com/spreadsheets/d/12OYrJzLVapSEWXMkmfQK-UbRS3j2JPFzwTZTv3DH6Zo/edit?usp=sharing <br>

<h2>2/ Trên môi trường triển khai thực tế:</h2>
<h3>2.1/ Kết nối dịch vụ Google:</h3>
* Yêu cầu cần có tài khoản Google Cloud. Mục đích: để truy cập Google Drive API, Google Sheet API và xuất data tin tức crawl được vào file Sheet quản lý <br>
- Truy cập Google Cloud Console: https://console.cloud.google.com/ <br>
- Tìm mục menu APIs & Services: chọn Enable APIs -> bật các API sau: <br>
    + Google Sheets API <br>
    + Google Drive API <br>
- Tìm menu APIs & Services: chọn mục Credentials -> Create Credentials -> Service Account -> Nhập thông tin để tạo tài khoản -> Done . Mục đích: tạo 1 tài khoản dịch vụ kết nối với API Google, tham khảo: https://stackoverflow.com/questions/46287267/how-can-i-get-the-file-service-account-json-for-google-translate-api <br>
- Trong Service Account -> Add Key -> Create new key -> lưu file JSON . File JSON này chứa các thông tin cần thiết để kết nối <br>
- Tải file .json về -> Đổi tên thành: `service_account.json` (nếu chọn tên khác thì chỉnh lại trong app.py) , sau đó đặt file này cùng thư mục với app.py. <br>
- Mở thử file `service_account.json`: tìm giá trị `client_email` -> copy nó lại (nó có dạng giống như abcxyz@name-app-123.iam.gserviceaccount.com) <br>
- Vào Google Drive -> tạo 1 file sheet mới -> Nhấn Chia sẻ -> Thêm email: paste cái client email khi nãy -> Cho phép chỉnh sửa -> Nhấn Xong để cập nhật quyền truy cập file Sheet <br>
- Copy ID file Sheet, tham khảo: https://stackoverflow.com/questions/36061433/how-do-i-locate-a-google-spreadsheet-id <br>
- Quay lại source code, tạo 1 file .env, mở file .env , copy code sau và paste vô, xong lưu lại: <br>
    
``` SHEET_ID = Id của file Sheet```

<h3>2.2/ Build Docker container (nên tìm một dịch vụ VPS rồi setup Docker trên VPS này nha):</h3>
- Cài đặt Docker:  <br>
    + VPS Windows: https://docs.docker.com/desktop/setup/install/windows-install/ <br>
    + VPS Linux: https://docs.docker.com/engine/install/ubuntu/ <br>
- Khởi chạy Docker <br>
- Build container với Command Prompt / Terminal: nhập `docker-compose build` -> Enter rồi đợi một lúc để khởi tạo container image <br>
- Chạy container: trong Command prompt / Terminal : nhập `docker-compose up -d` -> Enter <br>
- Kiểm tra container có chạy hay không: `docker ps` <br>

<h3>* Các yêu cầu tối thiểu đã có:</h3>
- Crawl data từ trang nguồn <br>
- Xuất data đã crawl vào tệp Google Sheet <br>
- Kiểm tra tin tức cũ trùng lặp trong Sheet <br>
- Đặt lịch thực thi crawl: `schedule.every(3).hours.do(crawl_news)` (thực thi sau mỗi 3 tiếng - miễn là Docker trên VPS và VPS luôn được bật) <br>
