# numRatings = 50000000
# covidSafeScore = 10.3 - ((132 + (-263)/(1 + pow((numRatings / 1592), 0.001977))) * 10)
# print(covidSafeScore)

import math
import psycopg2
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from populartimes_api import getPopularTimes

def calculateNumberOfReviewsCovidScore(numRatings):
    dangerScore = math.pow(math.e, 0.004 * numRatings) - 1
    if dangerScore >= 5:
        return 5
    else:
        return dangerScore

# NSW Health Score (/60)

def calculateNSWHealthCovidSafeScore(postcode):
    # Get number of covid cases in that postcode within 3 weeks
    print(os.getenv("db_password"))
    conn = psycopg2.connect(user="covidsafe",
                    password=os.getenv("db_password"),
                    host="localhost",
                    port="5432",
                    database="covidsafe")
    current_date = datetime.today()
    three_weeks_ago = current_date - timedelta(weeks=3)
    # Date format needs to be YYYY-MM-DD
    formatted_date = three_weeks_ago.strftime("%Y-%m-%d")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM infections WHERE postcode=%s AND notification_date >=%s", (str(postcode), formatted_date))
    data = cur.fetchall()
    print("DATA:")
    print(data[0][0])
    nsw_health_covid_score = data[0][0]
    modulated_covid_score = math.pow(math.e, 0.1 * nsw_health_covid_score) - 1
    return modulated_covid_score

def calculateTimeOfDayCovidSafeScore(place_id):
    popular_times = getPopularTimes(place_id)
    print(popular_times)

if __name__ == '__main__':
    load_dotenv()
    numRatings = 1181
    reviewScore = calculateNumberOfReviewsCovidScore(numRatings)
    healthScore = calculateNSWHealthCovidSafeScore(2170)
    total = reviewScore + healthScore
    calculateTimeOfDayCovidSafeScore("ChIJLynSq19fDWsRsvj0fl2_ODI")
    print(total)