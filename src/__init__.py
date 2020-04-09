from flask import Flask
from src.endpoints.routes import MESSAGES_API

# pylint: disable=C0103
app = Flask(__name__)
app.register_blueprint(MESSAGES_API)
print('Application initialized')
