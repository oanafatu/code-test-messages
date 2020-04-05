from flask import Flask


app = Flask(__name__)
print('Application initialized')

from src.endpoints import routes