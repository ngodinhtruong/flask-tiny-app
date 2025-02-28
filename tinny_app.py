from flask import Flask, redirect, url_for, render_template, request,session
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), unique=True, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, user_name, user_password, user_email):  
        self.user_name = user_name
        self.user_password = user_password
        self.user_email = user_email


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods = ['POST','GET'])
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

@app.route('/signup')
def signup():
    return render_template('logup.html')
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
