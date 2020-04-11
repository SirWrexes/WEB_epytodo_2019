from flask import Flask

app = Flask(__name__)
app.secret_key = "azerty"

from app import views