from app import app
from flask import request, render_template

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")