# # app.py deleted; run.py created
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
# from market import routes
#
# app = Flask(__name__)
# # database
# db = SQLAlchemy(app)  # initialised instance of SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
# app.config['SECRET_KEY'] = 'edf54dd3c3028392373f8682'
#
# # user password security : to generate hash passwords
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'edf54dd3c3028392373f8682'  # 'ec9439cfc6c796ae2029594d'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
# redirects user to login_page instead of market_page in case not logged in
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"  # displays log in message in blue color
from market import routes
