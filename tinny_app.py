from flask import Flask, redirect, url_for, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy

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
    errors = {"email": "", "password": ""}
    success = {"email": "", "password": ""}
    submitted = False  # Kiểm tra form đã submit chưa

    if request.method == 'POST':
        submitted = True  # Đánh dấu form đã submit

        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not first_name or not last_name or not email or not password or not confirm_password:
            flash("Lỗi: Vui lòng điền đầy đủ thông tin!", "error")
            return render_template('logup.html', errors=errors, success=success, submitted=submitted)

        full_name = first_name + " " + last_name  

        # Kiểm tra Email có tồn tại hay không
        existing_email = User.query.filter_by(user_email=email).first()
        if existing_email:
            errors["email"] = "Email đã tồn tại!"
            # success["email"] = "Email hợp lệ!"
        # Kiểm tra mật khẩu nhập lại có khớp không
        if password != confirm_password:
            errors["password"] = "Mật khẩu nhập lại không khớp!"

        if any(errors.values()):
            return render_template('logup.html', errors=errors, success=success, submitted=submitted)

        # Nếu mọi thứ hợp lệ, lưu vào database
        new_user = User(user_name=full_name, user_password=password, user_email=email)
        db.session.add(new_user)
        db.session.commit()

        flash("Đăng ký thành công! Hãy đăng nhập.", "success")
        return redirect(url_for('signin'))

    return render_template('logup.html', errors=errors, success=success, submitted=submitted)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
