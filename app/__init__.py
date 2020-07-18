from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "C\x07\xc2\x8c,a{My\x9f\xca\xe3.\x9b*\xef\xb6\xd6\xf3\x18\x82\xee\xbb\xd3"
# flask_app.config['CORS_HEADERS'] = 'Content-Type'

from app import routes

