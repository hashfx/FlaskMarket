from market import app, db
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user


# home page URL
@app.route('/')  # decorator
@app.route('/home')  # return same as in home page
def home_page():
    # return '<h1>Hello-World!</h1>'  # displays written text to the screen
    return render_template('home.html')  # handles requests and directs them into HTML files


"""
# dynamic routes
@app.route('/about/<username>')  # creates dynamic page URL
def about_page(username):  # takes username as argument
    # return '<h1>About Page!</h1>'
    return f'<h1>This page is about {username}</h1>'  # returns message with input username by user
"""


@app.route('/market', methods=['GET', 'POST'])
@login_required  # checks if user is logged in; if yes, returns user to market_page
def market_page():
    # items = [
    #     {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
    #     {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
    #     {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    # ]
    # fetch data from database
    # items = Item.query.all()  # returns all objects inside database
    # return render_template('market.html', items=items)
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":  # if clicked on Purchase/Sell button :: avoids displaying form-confirm-msg on refresh
        # Purchase Item Backend
        purchased_item = request.form.get('purchased_item')  # get purchased_item value
        p_item_object = Item.query.filter_by(name=purchased_item).first()  # get object of item from its value
        if p_item_object:  # check that purchase_item_object is not None
            # p_item_object.owner = current_user.id
            # current_user.budget -= p_item_object.price  # update budget
            # db.session.commit()  # save changes to database
            if current_user.can_purchase(p_item_object):  # check if item is affordable w.r.t. current budget
                p_item_object.buy(current_user)  # transfer ownership to buyer (current user)
                flash(f"Congratulations! You purchased {p_item_object.name} for ₹{p_item_object.price}",
                      category='success')
            else:  # in case of inadequate budget
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!",
                      category='danger')

        # Sell Item Backend
        sold_item = request.form.get('sold_item')  # get sold_item value
        s_item_object = Item.query.filter_by(name=sold_item).first()  # get object of item from its value
        if s_item_object:  # if sold_item object is not Null
            if current_user.can_sell(s_item_object):  # if user own the item, and want to sell; sell it
                s_item_object.sell(current_user)  # take-back ownership from buyer (current user) and set owner to None
                flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')

        return redirect(url_for('market_page'))  # redirect user to market_page after a transaction

    if request.method == "GET":  # avoids confirm-resubmission dialog box at refresh
        items = Item.query.filter_by(owner=None)  # remove item from available-items list
        owned_items = Item.query.filter_by(owner=current_user.id)  # update user market w.r.t. recent transactions
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items,
                               selling_form=selling_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email.data,
                              password_hash=form.password1.data)
        # add data to database
        db.session.add(user_to_create)
        db.session.commit()

        # log-in user as soon as they are registered
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')

        return redirect(url_for('market_page'))  # redirect to f(market_page) after validation

    # if validation fails, store it in form.errors
    if form.errors != {}:  # if no errors
        for err_msg in form.errors.values():  # iterate over validation errors
            # print(f'Validation Error UserCreation: {err_msg}')  # display validation error on terminal/shell
            flash(f'{err_msg}', category='danger')  # display validation error on page

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():  # if form is validated correctly
        attempted_user = User.query.filter_by(username=form.username.data).first()  # filter user by username
        # attempted_user = User.query.get(form.username.data).first()  # filter user by username

        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            # login user
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))  # once logged in; return user to market_page
        else:
            flash('Username and Password do not match! Try again!', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))
