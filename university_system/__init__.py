"""The university system flask application"""


from flask import Flask

app = Flask(__name__)

from . import routes
