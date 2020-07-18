from app import app, populartimes_api
from flask import request, render_template

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/populartimes", methods=['GET'])
def populartimes():
    place_id = request.args.get('place_id')
    return populartimes_api.getPopularTimes(place_id)