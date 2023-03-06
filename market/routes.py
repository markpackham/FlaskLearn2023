from flask import render_template, redirect, url_for, flash, request
from market import app
from market import db
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market.models import Item, User
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
# login_required prevents unauthorized users from accessing market
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()

    if request.method == "POST":
        # Purchase Item logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                # assign item ownership to user who purchased
                p_item_object.buy(current_user)
                flash(f'{p_item_object} purchased', category="success")
            else:
                flash(f'Sorry, you cannot afford that', category="danger")

        # Sell Item logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()

        if s_item_object:
            

        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)


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

        login_user(user_to_create)
        flash(f'You are now logged in as {user_to_create.username}', category='success')
        return redirect(url_for('market_page'))

    # form.errors is a builtin dictionary field
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    users = User.query.all()
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

    return render_template('login.html', form=form, users=users)


@app.route('/logout')
def logout_page():
    # this is a builtin function from flask_login
    logout_user()
    flash(f'You have been logged out', category='info')
    return redirect(url_for('home_page'))
