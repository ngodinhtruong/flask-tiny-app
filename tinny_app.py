from flask import Flask, redirect, url_for, render_template, request, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os

app = Flask(__name__)
app.secret_key = "secret"
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
    user_block = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"{self.username}"  # Sửa user_name thành username

    # Các phương thức cần cho Flask-Login (nếu dùng)
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
        new_user = User(user_name=f"{first_name} {last_name}", password=password, email=email)
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

    # if current_user.is_authenticated:
    #     return redirect(url_for('dashboard' if current_user.user_role == 'user' else 'admin'))  # Chuyển hướng nếu đã đăng nhập
    
    if request.method == 'POST':
        user_email = request.form['email_acc']
        user_pass = request.form['password_acc']
        # Nếu chưa nhập gì
        if user_email=='' or user_pass=='':
            session['error_message'] =  "Vui lòng nhập đầy đủ email và mật khẩu"
        else:
            if user_email and user_pass:
                user_sql = User.query.filter_by(email=user_email).first()
                if user_sql and user_sql.password == user_pass:
                    login_user(user_sql)
                    if user_sql.user_role == 1:
                        return redirect(url_for('admin'))
                    else:
                        return redirect(url_for('profile'))
                else:
                    session['error_message'] = 'Tai khoang hoac mat khau sai'
        return redirect(url_for('signin'))
                # return f'<h1> {user_email} </h1>'
    # session.pop()
    # error_message = 'khong co'
    error_message = session.pop('error_message', None)  # Xóa thông báo sau khi load trang
    return render_template('login.html', error_message=error_message)

@app.route('/logout')
@login_required
def log_out():
    logout_user()
    
    return redirect(url_for('signin'))

@app.route('/admin', methods=['POST','GET'])
@login_required
def admin():
    if request.method=='POST':
        if request.form.get('Đăng xuất') == 'Đăng xuất':
            return redirect(url_for('log_out'))
    return render_template('admin.html')

# Xóa định nghĩa Post thứ hai để tránh trùng lặp
# class Post(db.Model):
#     post_id = db.Column(db.Integer, primary_key = True)
#     title = db.Column(db.String(255), nullable = True)
#     content = db.Column(db.String(255), nullable = True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    
#     def __init__(self, title, content, user_id):
#         self.title = title
#         self.content = content
#         self.user_id = user_id

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_posts = Post.query.filter_by(user_id=current_user.user_id).all()
    all_posts = Post.query.all()
    
    if request.method == "POST":
        if request.form.get("Đăng xuất") == "Đăng xuất":
            return redirect(url_for("log_out"))
        if 'them_bai_viet' in request.form:
            session['bai_viet'] = True
            return redirect(url_for('profile'))
        if 'Close_app' in request.form:
            session.pop('bai_viet')
        if request.form.get("accept") == "submit":
            title = request.form.get("title")
            content = request.form.get("content")
            if not title and not content:
                return render_template("profile.html",
                                post = all_posts,
                                them_bai_viet = True,
                                error_no_content = 'Vui lòng nhập đầy đủ <span style = "">tiêu đề</span> và <span>nội dung</span>')
            # Tạo bài viết mới và lưu vào DB
            new_post = Post(
                user_id=current_user.user_id,
                title=title,
                content=content
            )
            db.session.add(new_post)
            db.session.commit()

            session.pop('bai_viet', None)
            return redirect(url_for('profile'))
        
    bai_viet = session.pop('bai_viet', False)
    return render_template("profile.html", posts=all_posts, them_bai_viet=bai_viet)

@app.route("/add_post", methods=["GET", "POST"])
@login_required
def add_content():

    pass

@app.route("/delete", methods=["POST"], endpoint="delete_pop")
@app.route("/delete/<int:post_id>", methods=["POST"], endpoint="delete_pop")
@login_required
def delete_pop(post_id=None):
    if post_id:
        post = Post.query.filter_by(post_id=post_id, user_id=current_user.user_id).first()
        if post:
            db.session.delete(post)
            db.session.commit()
            flash("Bài viết đã được xóa thành công!", "success")
        else:
            flash("Bài viết không tồn tại hoặc bạn không có quyền xóa!", "warning")
    else:
        selected_ids = request.form.getlist("post_id")
        if selected_ids:
            Post.query.filter(Post.post_id.in_(selected_ids), Post.id == current_user.user_id).delete(synchronize_session=False)
            db.session.commit()
            flash("Các bài viết đã được xóa thành công!", "success")
        else:
            flash("Vui lòng chọn ít nhất một bài viết để xóa!", "warning")
    return redirect(url_for("profile"))

@app.route("/edit/<int:post_id>", methods=["GET", "POST"], endpoint="edit_post")
@login_required
def edit_post(post_id):
    post = Post.query.filter_by(post_id=post_id, user_id=current_user.user_id).first()
    if not post:
        flash("Bài viết không tồn tại hoặc bạn không có quyền chỉnh sửa!", "warning")
        return redirect(url_for("profile"))
    
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if title and content:
            post.title = title
            post.content = content
            db.session.commit()
            flash("Bài viết đã được cập nhật thành công!", "success")
            return redirect(url_for("profile"))
        else:
            flash("Vui lòng nhập đầy đủ tiêu đề và nội dung!", "warning")
    
    return render_template("edit_post.html", post=post)


@app.route('/',methods=['POST','GET'])
def home():
    if request.method=='POST':
        if request.form.get('sign in') == 'Sign in':
            return redirect(url_for('signin'))
    return render_template('top_home.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)