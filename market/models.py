from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin  # for is_active, is_authenticated, is_anonymous, get_id

# navigation through different pages, after authentication, is refresh
# each refresh is different request session for flask
# checks if user is logged in or not after each refresh


#
@login_manager.user_loader
def load_user(user_id):
    # return User.get(user_id)
    return User.query.get(int(user_id))


# database to store user information
class User(db.Model, UserMixin):  # UserMixin => [{is_active}, {is_authenticated}, {is_anonymous}, {get_id}]
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=32), nullable=False, unique=True)
    email_address = db.Column(db.String(length=48), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)  # hashed password length = 60
    budget = db.Column(db.Integer(), nullable=False, default=25000)
    items = db.relationship('Item', backref='owned_user', lazy=True)  # returns name_of_user(owner) of item_name(item)

    @property
    def prettier_budget(self):  # add a comma between digits if num_of_digit >= 4
        if len(str(self.budget)) >= 4:
            return f'₹{str(self.budget)[:-3]},{str(self.budget)[-3:]}'  # $
        else:
            return f"₹{self.budget}"

    @property
    def password_hash(self):
        return self.password_hash

    @password_hash.setter
    def password_hash(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)  # check if password already exists

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price  # return bool value : if item is affordable

    def can_sell(self, item_obj):
        return item_obj in self.items  # return bool value : verify if user owns the item


# database Model class
class Item(db.Model):
    # Column(datatype=String; len_of_char=32; cannot_be_null; isUnique1)
    id = db.Column(db.Integer(), primary_key=True)  # primary key
    name = db.Column(db.String(length=32), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'  # returns Item name_col_of_database

    def buy(self, user):
        self.owner = user.id  # transfer ownership to user with user.id
        user.budget -= self.price  # decrease budget w.r.t. item price
        db.session.commit()  # update database

    def sell(self, user):
        self.owner = None  # revert ownership to None
        user.budget += self.price  # increase budget w.r.t. item price
        db.session.commit()  # update database
