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
    # errors = {"email": "", "password": ""} # No keu la no luu lai 
    # success = {"email": "", "password": ""}

    if request.method == 'POST':

        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not first_name or not last_name or not email or not password or not confirm_password:
            flash("Lỗi: Vui lòng điền đầy đủ thông tin!", "error")
            return render_template('logup.html')

        full_name = first_name + " " + last_name  

        # Kiểm tra Email có tồn tại hay không
        existing_email = User.query.filter_by(user_email=email).first()
        if existing_email:
            session["error"] = "Email đã tồn tại!"
            # success["email"] = "Email hợp lệ!"
        # Kiểm tra mật khẩu nhập lại có khớp không
        if password != confirm_password:
            session["error"] = "Mật khẩu nhập lại không khớp!"

        if any(session.values()):
            return render_template('logup.html')

        # Nếu mọi thứ hợp lệ, lưu vào database
        new_user = User(user_name=full_name, user_password=password, user_email=email)
        db.session.add(new_user)
        db.session.commit()
        

        flash("Đăng ký thành công! Hãy đăng nhập.", "success")
        return redirect(url_for('signup'))
    
    errors = session.pop('error',None)
    return render_template('logup.html', errors=errors)

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
