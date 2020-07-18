# numRatings = 50000000
# covidSafeScore = 10.3 - ((132 + (-263)/(1 + pow((numRatings / 1592), 0.001977))) * 10)
# print(covidSafeScore)

import math
import psycopg2
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from app import populartimes_api

# Score based on number of reviews/popularity on google places 5%

def calculateNumberOfReviewsCovidScore(numRatings):
    dangerScore = math.pow(math.e, 0.004 * numRatings) - 1
    if dangerScore >= 5:
        return 5
    else:
        return dangerScore

# NSW Health Score 60%

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

# Score based on current popularity level 25%
def calculateTimeOfDayCovidSafeScore(place_id):
    popular_times = populartimes_api.getPopularTimes(place_id)
    print(popular_times)
    current_time = datetime.now()
    current_day = current_time.weekday()
    current_hour = current_time.hour
    # weekday_map = {
    #     0 : "Monday",
    #     1 : "Tuesday",
    #     2 : "Wednesday",
    #     3 : "Thursday",
    #     4 : "Friday",
    #     5 : "Saturday",
    #     6 : "Sunday"
    # }
    # weekday = weekday_map.get(current_day)
    return popular_times['populartimes'][current_day]['data'][current_hour]

# Score based on ratings from users of our app (users can rate the covid safety of a particular location) 10%
def calculateUserRatings(place_id):
    conn = psycopg2.connect(user="covidsafe",
                            password=os.getenv("db_password"),
                            host="localhost",
                            port="5432",
                            database="covidsafe")
    cur = conn.cursor()
    cur.execute("SELECT * FROM ratings WHERE place_id=%s", (place_id,))
    data = cur.fetchall()
    if len(data) == 0:
        return -1
    else:
        print(data)
        return sum([int(x) for x in data[0][1]])/len(data[0][1])

