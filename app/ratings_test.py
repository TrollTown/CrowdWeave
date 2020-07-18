# numRatings = 50000000
# covidSafeScore = 10.3 - ((132 + (-263)/(1 + pow((numRatings / 1592), 0.001977))) * 10)
# print(covidSafeScore)

import math
import psycopg2
from datetime import datetime, timedelta
import os

def calculateNumberOfReviewsCovidScore(numRatings):
    dangerScore = math.pow(math.e, 0.004 * numRatings) - 1
    if dangerScore >= 5:
        return 5
    else:
        return dangerScore

# NSW Health Score (/60)

def calculateNSWHealthCovidSafeScore(postcode):
    # Get number of covid cases in that postcode within 3 weeks
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
    cur.execute("SELECT COUNT(*) FROM infections WHERE postcode=%s AND notification_date >=%s", (postcode, formatted_date))
    data = cur.fetchall()
    print("DATA:")
    print(data)
    return 0

if __name__ == '__main__':
    numRatings = 1181
    reviewScore = calculateNumberOfReviewsCovidScore(numRatings)
    healthScore = calculateNSWHealthCovidSafeScore(2154)
    total = reviewScore + healthScore
    print(total)