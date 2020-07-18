from app import app, populartimes_api, database
from flask import request, render_template

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/populartimes", methods=['GET'])
def populartimes():
    place_id = request.args.get('place_id')
    return populartimes_api.getPopularTimes(place_id)

@app.route("/covidsafeScore", methods=['GET'])
def covidsafeScore():
    place_id = request.args.get('place_id')
    # Get number of google reviews
    populartimes_result = populartimes_api.getPopularTimes(place_id)
    numRatings = populartimes_result['rating_n']
    covidSafeScore = 10.3 - ((132 + (-263)/(1 + pow((numRatings / 1592), 0.001977))) * 10)
    postcode = populartimes_result['address'][4:]
    command = 'SELECT * FROM infections WHERE postcode=%s'
    values = (postcode,)
    db_result = database.fetch(command, values)
    if (len(db_result) != 0):
        covidSafeScore = covidSafeScore / 2
    return {
        "score": covidSafeScore
    }

@app.route("/rating", methods=['GET', 'POST'])
def saveCovidSafeScore():
    # Handle GET case
    if request.method == 'GET':
        return {
            "rating" : 75
        }
    # Handle POST case
    place_id = request.args.get('place_id')
    rating = request.args.get('rating')
    command = "INSERT INTO ratings VALUES(%s, %s)"
    values = (place_id, rating)
    database.execute(command, values)
    
    