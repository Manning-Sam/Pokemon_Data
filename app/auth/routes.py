from flask import Blueprint,render_template,request, redirect, url_for
from werkzeug.security import check_password_hash
from .forms import LoginForm, UserInfoForm
from app.models import User,Post
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth',__name__,template_folder='auth_templates')

from app.models import db

@auth.route('/login', methods=["GET","POST"])
def logMeIn():
    form = LoginForm()
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data

        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            print("wrong password")
            return redirect(url_for('login.html'))

        login_user(user, remember=remember_me)
        return redirect(url_for('home'))

    return render_template('login.html', form = form)
        



@auth.route('/signup', methods =["GET", "POST"])
def signUp():
    signup_form = UserInfoForm()
    if request.method == "POST":
        if signup_form.validate():
            print('form was validated')
            username = signup_form.username.data
            email = signup_form.email.data
            password = signup_form.password.data

            user = User(username, email, password)
            db.session.add(user)
            db.session.commit()
        
            return redirect(url_for('home'))
        else: 
            print("not validated")

    return render_template('signup.html', form = signup_form)

@auth.route('/logout')
def logMeOut():
    logout_user()
    return redirect(url_for('auth.logMeIn'))