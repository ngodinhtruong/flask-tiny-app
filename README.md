# Flask_tinny_app: blog

## 1. Thông tin thành viên

- Ngô Trường Định - 2264171
- Phan Thành Đạt - 22641631

## 2. Thông tin project

Dự án là một ứng dụng web (webapp) cho phép người dùng (user) tạo, quản lý blog cá nhân và quản trị viên (admin) giám sát, quản lý người dùng cũng như nội dung trên hệ thống. Ứng dụng được xây dựng với mục tiêu cung cấp giao diện đơn giản, dễ sử dụng, đồng thời đảm bảo tính năng cơ bản của một hệ thống blog như đăng bài, chỉnh sửa, xóa bài và phân trang.

**Công nghệ sử dụng**

- **Backend**: Flask (Python framework)
  - Flask được chọn nhờ tính nhẹ nhàng, dễ mở rộng và phù hợp cho các dự án nhỏ đến trung bình. Backend xử lý logic nghiệp vụ, định tuyến (routing), và tương tác với cơ sở dữ liệu.
- **Frontend**: HTML & CSS
  - HTML dùng để cấu trúc giao diện, CSS dùng để tùy chỉnh kiểu dáng, đảm bảo giao diện thân thiện và responsive trên các thiết bị.
- **Database**: SQLite
  - SQLite là cơ sở dữ liệu nhẹ, không cần server riêng, phù hợp cho ứng dụng quy mô nhỏ. Dữ liệu bao gồm thông tin người dùng, bài viết và các cấu hình cơ bản.

**Các tính năng chính**

1. **Phân quyền người dùng**

   - **User (Người dùng thông thường)**:
     - Đăng ký, đăng nhập để quản lý blog cá nhân.
     - Tạo bài viết mới, xóa bài viết của chính mình.
     - Xem danh sách bài viết với phân trang (pagination).
   - **Admin (Quản trị viên)**:
     - Đăng nhập vào bảng điều khiển (dashboard) riêng.
     - Quản lý danh sách người dùng: xem, khóa/mở khóa tài khoản.
     - Giám sát bài viết: xóa bài viết không phù hợp (nếu cần).
2. **Quản lý bài viết**

   - Người dùng có thể:
     - Đăng bài với tiêu đề, nội dung (text).
     - Xóa bài viết đã đăng.
   - Hiển thị danh sách bài viết (blog posts) hỗ trợ phân trang để dễ theo dõi.
3. **Giao diện**

   - Trang cá nhân: Hiển thị thông tin user và bài viết của họ.
   - Trang admin: Dashboard với bảng danh sách user và công cụ quản lý.

**Cấu trúc dự án**

- **Backend (Flask)**:

  - File chính: `tinny_app.py` (chứa logic Flask, định tuyến, xử lý request).
  - Tích hợp SQLite qua thư viện `sqlite3` hoặc ORM như SQLAlchemy (tùy chọn).
- **Frontend (HTML/CSS)**:

  - Thư mục `templates/`:
    - `home.html`: Trang chủ hiển thị bài viết.
    - `login.html`: Form đăng nhập.
    - `logup.html`: Form đăng ký.
    - `user.html`: Trang cá nhân của user.
    - `admin.html`: Dashboard cho admin.
    - `top_home.html`: phần top cho mỗi trang.
  - Thư mục `static/`:
    - `style.css`: CSS chung cho toàn bộ ứng dụng.
    - `style_user.css`, `style_admin.css`: CSS tùy chỉnh cho từng vai trò.
- **Database (SQLite)**:

  - File: `database/mydatabase.db`.
  - Bảng chính:
    - `users`: Lưu thông tin người dùng (id, username, password,user_role,user_block).
    - `posts`: Lưu bài viết (id, title, content, user_id).

**Quy trình hoạt động**

1. Người dùng đăng ký tài khoản và đăng nhập.
2. Sau khi đăng nhập, user có thể tạo bài viết mới hoặc xóa bài cũ từ trang cá nhân.
3. Trang chủ hiển thị tất cả bài viết của user với phân trang (ví dụ: 10 bài/trang).
4. Admin đăng nhập vào dashboard, xem danh sách user và thực hiện quản lý (khóa tài khoản, đặt lại mật khẩu cho user).

## 3. Cách cài đặt project

**1. Docker**

- pull: `docker pull zsaber/flask_tinny_app:latest`
- run:  `docker run -d -p 5000:5000 flask_tiny_app`

**2. Window**
- run  `setup_ex1.bat`

**3. Ubuntu/linux**
- run  `setup_ex1.sh`
- run  `setup_ex1.zsh`

## 4. Triển khai project
 - Nền tảng: `Pythoanywhere`
 - Link: `https://ngotruongdinh.pythonanywhere.com/signin`
 - github: `https://github.com/ngodinhtruong/flask-tiny-app/blob/master`
