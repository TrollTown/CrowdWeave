import livepopulartimes, json

def getPopularTimes(id):
    result = livepopulartimes.get_populartimes_by_PlaceID("AIzaSyASUNkGuA2TVIMetjobbJTAgyz6y29b4bE", id)
    return result


if __name__ == '__main__':
    print(json.dumps(getPopularTimes("ChIJQXBWbSCjEmsRV51peXqvQJ0")))