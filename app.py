from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for, session, \
    flash
from warrant import Cognito
from settings import *
from botocore.exceptions import ClientError

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
u = Cognito(USER_POOL_ID, CLIENT_ID, user_pool_region=REGION)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup')
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']  # hashed in warrant
        password_confirm = request.form['confirm_password']
        if password != password_confirm:
            flash("Passwords don't match!")
            return redirect(url_for('signup'))
        u.add_base_attributes(email=email)
        try:
            u.register(username, password)
            return redirect(url_for("confirm_signup", username=username,
                                    password=password))
        except ClientError as e:
            flash(e.response.get('Error').get('Message'))

    return render_template("signup.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/confirm_signup/<username>', methods=['POST', 'GET'])
def confirm_signup(username):
    if request.method == 'POST':
        code = request.form['confirm_code']
        u = Cognito(USER_POOL_ID, CLIENT_ID, REGION, username=username,
                    access_key='dummy_not_used', secret_key='dummy_not_used')
        try:
            u.confirm_sign_up(code, username=username)
        except ClientError as e:
            flash(e.response.get('Error').get('Message'))
            return redirect(url_for('confirm_signup', username=username))
        return redirect(url_for('login', username=username))

    return render_template('confirm_signup.html')
if __name__ == '__main__':
    app.run(debug=True)
