from flask import Flask, redirect, url_for, render_template, request
 
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods = ['POST','GET'])
def signin():
    if request.method == 'POST':
        user_email = request.form['email_acc']
        user_pass = request.form['password_acc']
        if user_email and user_pass:
            return f'<h1> {user_email} </h1>'
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('logup.html')
if __name__ == '__main__':
    app.run(debug=True)
