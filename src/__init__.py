from flask import Flask

# pylint: disable=C0103
app = Flask(__name__)
print('Application initialized')

# pylint: disable=wrong-import-position
from src.endpoints import routes
