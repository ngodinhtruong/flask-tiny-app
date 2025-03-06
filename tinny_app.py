from flask import Flask, redirect, url_for, render_template, request, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import make_response
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)


# 🔥 Khởi tạo LoginManager đúng cách
login_manager = LoginManager()
login_manager.init_app(app)  # Đúng cách!
login_manager.login_view = 'signin'  # Nếu chưa đăng nhập, chuyển hướng đến login
login_manager.login_message_category = 'info'

# Chỉ định thư mục database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, 'database')
os.makedirs(DB_DIR, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(DB_DIR, "mydatabase.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)  # Cho phép họ tên giống nhau
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email phải là duy nhất
    user_role = db.Column(db.Integer, nullable=False, default=0)
    user_block = db.Column(db.Integer, nullable=False, default=0)
    def __repr__(self):
        return f'{self.username}'

    def get_id(self):
        return str(self.id)

    
# user từ database
class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Sửa 'user.user_id' thành 'users.id'
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post(id={self.post_id}, title={self.title})"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Tìm user theo ID


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    errors = {}  #Đây là biến lỗi để lưu được nhiều lỗi xuất hiện cũng lúc 
    form_data = session.get("form_data", {"firstname": "", "lastname": "", "email": ""}) # Lấy dữ liệu từ session và hiển thị lại form nếu có lỗi

    if request.method == 'POST':
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not first_name or not last_name or not email or not password or not confirm_password:
            errors["general"] = "Vui lòng nhập đầy đủ thông tin!"

        if password and confirm_password and password != confirm_password:
            errors["confirm_password"] = "Mật khẩu không trùng khớp!"

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            errors["email"] = "Email đã tồn tại!"

        # Kiểm tra các lỗi tồn tại trong secssion
        if errors:
            session["form_data"] = {
                "firstname": first_name if "firstname" not in errors else "",
                "lastname": last_name if "lastname" not in errors else "",
                "email": email if "email" not in errors else ""
            }
            session["errors"] = errors
            return redirect(url_for('signup'))

        # Lưu
        new_user = User(username=f"{first_name} {last_name}", password=password, email=email)
        db.session.add(new_user)
        db.session.commit()

        session.pop("form_data", None)
        session.pop("errors", None)

        flash("Đăng ký thành công! Hãy đăng nhập.", "success")
        return redirect(url_for('signin'))

    form_data = session.pop("form_data", {"firstname": "", "lastname": "", "email": ""})
    errors = session.pop("errors", {})

    return render_template('logup.html', errors=errors, form_data=form_data)



@app.route('/signin', methods = ['POST','GET'])
def signin():
    if 'user' in session:
        if session['user'] == True:
            return redirect(url_for('admin'))
        return redirect(url_for('home'))

    if request.method == 'POST':
        user_email = request.form['email_acc']
        user_pass = request.form['password_acc']
        # Nếu chưa nhập gì
        if user_email=='' or user_pass=='':
            session['error_message'] =  "Vui lòng nhập đầy đủ email và mật khẩu"
            return redirect(url_for('signin'))
        user_sql = User.query.filter_by(email=user_email).first()
        if user_sql and user_sql.password == user_pass:
            if user_sql.user_block == 1:
                session['error_message'] = 'Tài khoảng của bạn đã bị chặn'
                return redirect(url_for('signin'))
            login_user(user_sql, remember=True)
            if user_sql.user_role == 1:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('user'))
        session['error_message'] = 'Tài khoảng hoặc mật khẩu sai'

        return redirect(url_for('signin'))
               
    error_message = session.pop('error_message', None)  # Xóa thông báo sau khi load trang
    session.clear()
    return render_template('login.html', error_message=error_message)

@app.route('/logout')
@login_required
def log_out():
    logout_user()  # Xóa trạng thái đăng nhập của Flask-Login
   
    return redirect(url_for('signin'))

@app.route('/admin', methods=['POST','GET'])
@login_required
def admin():
    if request.method=='POST':
        if request.form.get('Đăng xuất')== 'logout':
            return redirect(url_for('log_out'))
        if 'user_id' in request.form:
            print('request.form: ',request.form)
            user_id = int(request.form['user_id'])
            user_block_change = 0 if 'user_block' in request.form else 1
            user_sql = User.query.get(user_id)

            if 'reset-password' in request.form:
                default_password = 123
                if user_sql:
                    user_sql.password = default_password
                    db.session.commit()
            if user_sql:
                user_sql.user_block = user_block_change
                db.session.commit()
            return redirect(url_for('admin'))
    all_user = User.query.filter(User.user_role != 1).all()
    
    active_users = User.query.filter(User.user_block == 0, User.user_role != 1).count()
    return render_template('admin.html', rows = all_user,active_users = active_users)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def user():
    all_posts = Post.query.filter_by(user_id=current_user.id).all()
    all_posts_page = []
    post_per_page = []

    for post in range(len(all_posts)):
        post_per_page.append(all_posts[post])
        if (post+1)%10==0:
            all_posts_page.append(post_per_page)
            post_per_page = []
    if post_per_page:  # If there are remaining posts in post_per_page
        all_posts_page.append(post_per_page)
    if request.method == "POST":

        if 'next_page' in request.form:
            current_page = int(request.form['next_page'])
            if current_page == len(all_posts_page):
                session['current_page'] = current_page
            session['current_page'] = current_page+1

        if 'pre_page' in request.form:
            current_page = int(request.form['pre_page'])
            if current_page == 1:
                session['current_page'] = 1
            session['current_page'] = current_page-1

        if request.form.get("Đăng xuất") == "Đăng xuất":
            return redirect(url_for("log_out"))
        if 'them_bai_viet' in request.form:
            session['them_bai_viet'] = True
            return redirect(url_for('user'))
        if 'Close_app' in request.form:
            session.pop('them_bai_viet',False)

        # Xử lý nút xóa
        if 'xoa_bai_viet' in request.form:
            session['xoa_bai_viet'] = True
            return redirect(url_for('user'))
        
        # Xử lý xác nhận xóa
        if 'xac_nhan_xoa' in request.form:
            selected_posts = request.form.getlist('delete_posts')
            print(selected_posts)  # Lấy danh sách ID bài được chọn
            if selected_posts:
                for post_id in selected_posts:
                    post = Post.query.get(post_id)
                    if post and post.user_id == current_user.id:  # Kiểm tra quyền
                        db.session.delete(post)
                db.session.commit()
            session.pop('xoa_bai_viet', False)
            return redirect(url_for('user'))
        

        if request.form.get("accept") == "submit":
            title = request.form.get("title")
            content = request.form.get("content")
            print(title,content)
            if not title or not content:
                flash('Vui lòng nhập đầy đủ tiêu đề và nội dung', 'danger')
                current_page = session.pop('current_page',1)
                if not all_posts_page:
                    display_post = []
                else:
                    display_post = all_posts_page[current_page-1]
                return render_template("user.html", posts=display_post, them_bai_viet=True,current_page = current_page,max_page = len(all_posts_page), email = current_user.email, name=current_user.username)

            else:   
                new_post = Post(
                    user_id=current_user.id,
                    title=title,
                    content=content
                )
                db.session.add(new_post)
                db.session.commit()

                session.pop('them_bai_viet', False)
            return redirect(url_for('user'))
    
    current_page = session.pop('current_page',1)
    them_bai_viet = session.pop('them_bai_viet', False)
    xoa_bai_viet = session.get('xoa_bai_viet', False)
    if not all_posts_page:
        display_post = []
    else:
        display_post = all_posts_page[current_page-1]
    return render_template("user.html", posts=display_post, them_bai_viet=them_bai_viet, xoa_bai_viet = xoa_bai_viet,current_page = current_page,max_page = len(all_posts_page), email = current_user.email, name=current_user.username)








@app.route('/',methods=['POST','GET'])
def home():
    if request.method=='POST':
        if request.form.get('sign in') == 'Sign in':
            return redirect(url_for('signin'))
    return render_template('top_home.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Kiểm tra và tạo user admin nếu chưa có
        admin_user = User.query.filter_by(user_role=1).first()
        if not admin_user:
            default_admin = User(
                username="admin",
                password="admin",  # Lưu ý: Nên mã hóa password trong thực tế
                email="admin@admin.admin",
                user_role=1,  # Vai trò admin
                user_block=0  # Không bị chặn
            )
            db.session.add(default_admin)
            db.session.commit()
            print("Đã tạo user admin mặc định: admin/admin123")
    app.run(debug=True)