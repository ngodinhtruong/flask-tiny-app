from flask import Flask, redirect, url_for, render_template, request, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)  # Cho phép họ tên giống nhau
    user_password = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), unique=True, nullable=False)  # Email phải là duy nhất

    def __init__(self, user_name, user_password, user_email):  
        self.user_name = user_name
        self.user_password = user_password
        self.user_email = user_email

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

        existing_email = User.query.filter_by(user_email=email).first()
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
        new_user = User(user_name=f"{first_name} {last_name}", user_password=password, user_email=email)
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
    
    if request.method == 'POST':
        user_email = request.form['email_acc']
        user_pass = request.form['password_acc']
        # Nếu chưa nhập gì
        if user_email=='' or user_pass=='':
            session['error_message'] =  "Vui lòng nhập đầy đủ email và mật khẩu"
        else:
            if user_email and user_pass:
                user_sql = User.query.filter_by(user_email=user_email).first()
                if user_sql and user_sql.user_password == user_pass:
                    return redirect(url_for('home'))
                else:
                    session['error_message'] = 'Tai khoang hoac mat khau sai'
        return redirect(url_for('signin'))
                # return f'<h1> {user_email} </h1>'
    # session.pop()
    # error_message = 'khong co'
    error_message = session.pop('error_message', None)  # Xóa thông báo sau khi load trang
    return render_template('login.html', error_message=error_message)

@app.route('/')
def home():
    return render_template('index.html')
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
