from app import app, populartimes_api, database, score_calculator
from flask import request, render_template

import requests

import os

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
    print("TTTTTTTTTTTTTTTTTTTTTTTTTTTT")
    if populartimes_result == None:
        res = requests.get('https://maps.googleapis.com/maps/api/place/details/json?key=%s&place_id=%s', (os.getenv("GOOGLE_API_KEY"), place_id))
        if res.status_code != 200:
            postcode = -1
            print("NOOOOOOOOOOOOO")
        else:
            j = res.json()
            print(j)
            print("hello world")
    try:
        numRatings = populartimes_result['rating_n']
    except KeyError as e:
        print("KeyError")
        print(e)
        numRatings = -1
    reviewScore = score_calculator.calculateNumberOfReviewsCovidScore(numRatings)

    postcode = populartimes_result['address'][4:]
    healthScore = score_calculator.calculateNSWHealthCovidSafeScore(postcode)
    popularTimesScore = score_calculator.calculateTimeOfDayCovidSafeScore(place_id)
    userRatingScore = score_calculator.calculateUserRatings(place_id)
    allScores = [reviewScore, healthScore, popularTimesScore, userRatingScore]
    scoreWeights = [5, 60, 25, 10]
    totalWeight = 0
    totalScore = 0
    for i in range(len(allScores)):
        if allScores[i] != -1:
            totalWeight += scoreWeights[i]
            totalScore += allScores[i]
        else:
            print("we hit a -1")
    if totalWeight == 0:
        return 10    # If no information available at all then it is likely the place is reasonably covid safe
    scaledCovidScore = (totalScore/totalWeight) * 100 # Otherwise return the weighted covid score
    return {
        "score": round(scaledCovidScore)
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
