"""The university system flask application"""


from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = "very_secret_key;believe_me"

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

bootstrap5 = Bootstrap5()
bootstrap5.init_app(app)

from . import routes
