from flask import render_template, redirect, url_for, flash
from market import app
from market import db
from market.forms import RegisterForm, LoginForm
from market.models import Item, User
from flask_login import login_user, logout_user


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              # user password.setter rather than password_hash field
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))

    # form.errors is a builtin dictionary field
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    # check all info if valid and is triggered when we hit submit button on form
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correct(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Login Successful, you are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash(f'Login params invalid', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    # this is a builtin function from flask_login
    logout_user()
    flash(f'You have been logged out', category='info')
    return redirect(url_for('home_page'))
