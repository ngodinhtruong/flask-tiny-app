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

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)  # Cho phép họ tên giống nhau
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email phải là duy nhất
    user_role = db.Column(db.Integer, nullable=False, default=0)
    user_block = db.Column(db.Integer, nullable=False, default=0)
    def __repr__(self):
        return f'{self.username}'
# Fix lỗi: Thiết lập user_loader để Flask-Login có thể tìm 
# user từ database
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
        new_user = User(username=f"{first_name} {last_name}", password=password, email=email,user_role = 0,user_block = False)
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
                return redirect(url_for('home'))
        session['error_message'] = 'Tài khoảng hoặc mật khẩu sai'
        return redirect(url_for('signin'))
               
    error_message = session.pop('error_message', None)  # Xóa thông báo sau khi load trang
    session.clear()
    return render_template('login.html', error_message=error_message)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


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
    print(session)
    all_user = User.query.all()
    return render_template('admin.html', rows = all_user)


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
