#(c) 2020 nathan thimothe
import os
import requests
import subprocess
import json
import random
import credentials
import textwrap
from datetime import datetime, timedelta


TAGS = ['clear', 'cloud', 'rain', 'bright', 'fog']

IMG_EXTENSIONS = ['png', 'jpg', 'jpeg', 'tiff']
headers = {
    'x-rapidapi-host': credentials.RAPID_API_HOST,
    'x-rapidapi-key':  credentials.RAPID_API_KEY
    }

URL = "https://" + headers['x-rapidapi-host'] + "/weather"

def getLocation():
    # run the whereami command line tool
    process = subprocess.run(['whereami'],
                             stdout=subprocess.PIPE,
                             universal_newlines=True)

    text = process.stdout.splitlines()

    map = dict()
    # get latitude and longitude
    for i in range(2):
        items = text[i].split(":")
        # make sure to let lat and lon as floats
        map[items[0]] = float(items[1].strip())

    return map


def detectWeather(lat, lon, city = None):
    """
    Make request to Rapid API for the weather of a specific city, and return the JSON output.
    """
    query = {"mode": "json", "units": "imperial", "lat": lat, "lon": lon}

    if city is not None:
        query = {"mode": "json", "units": "imperial", "q": city}

    req = requests.request("GET", URL, headers = headers, params = query)

    if req.status_code != 200:
        print("API Exception")
        quit()

    return json.loads(req.text)



def timeCategory(sunrise, sunset):
    """
    Determine which time of day it is: night, sunrise, day, or sunset, given the sunrise and sunset datetime objects.
    """
    now = datetime.today()
    hour = timedelta(hours = 1)
    twoHours = timedelta(hours = 2)
    #  all times one before sunrise AND all times two hours after sunset (inclusive) should be classified as "night"
    if now < sunrise-hour or now >= sunset+twoHours:
        return "night"

    # if it's anywhere from an hour before sunrise to 2 hours before sunrise, call it "sunrise"
    elif now >= sunrise-hour and now <= sunrise+twoHours:
        return "sunrise"

    # it's currently two hours or more after sunrise and an hour before sunset (exclusive), it's day
    elif now >= sunrise+twoHours and now < sunset-hour :
        return "day"

    # if it's anywhere from an hour before sunset to 2 hours after sunset, call it "sunset"
    elif now >= sunset-hour and now <= sunset+twoHours:
        return "sunset"


def parseKeyWords(json_response):
    """
    Given a dictionary object, match its key words to TAGS constant.
    """
    timeOfDay = timeCategory(sunrise = datetime.fromtimestamp(json_response['sys']['sunrise']), sunset = datetime.fromtimestamp(json_response['sys']['sunset']))

    description = json_response['weather'][0]['main'].strip().lower()

    keyWords = [timeOfDay]

    for tag in TAGS:
        if tag in description:
            keyWords.append(tag)
            break


    return keyWords


def getBackgroundsPath(keywords):
    """
    Given a list of key words, navigate to the correct path in the directory.
    """
    # get the images associated with this particular time of day
    timePath = (os.path.join("Wallpapers",keywords[0]))

    # first keyword gives more important weather information
    tagPath = os.path.join(timePath, keywords[1])
    return tagPath

def setBackground(keywords):
    # get all eligible backgrounds
    path = os.path.join(os.getcwd(), getBackgroundsPath(keywords))
    validBackgrounds = []
    for each in os.listdir(path):
        if each.split(".")[-1].lower().strip() in IMG_EXTENSIONS:
            validBackgrounds.append(each)

    # pick a random one
    backgroundToSet = validBackgrounds[random.randint(0, len(validBackgrounds)-1)]


    # set the background

    # define apple script command using osascript
    SCRIPT = """osascript -e 'tell application "Finder" to set desktop picture to "%s" as POSIX file'"""

    # run process
    process = subprocess.Popen(SCRIPT%os.path.join(path,backgroundToSet), shell=True)


def help():
    return """
If you're having any trouble, make sure to authorize the whereami command-line tool. Also, if you've added any images to any directories, make sure that they're either .png, .jpg, .jpeg, or .tiff.

Run the program as follows:
      python3 weatherBackground.py
OR

./install.sh will install all dependencies and add a job to your cronjob using a file named "weather.cron "to make sure the program runs daily.

"""


if __name__ == "__main__":
    import sys
    import argparse

    # parse arguments
    parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter, description='Change your Mac OS background based on the weather of your current city and the time.', epilog = textwrap.dedent(help()))
    
    parser.parse_args()
    
    location = getLocation()

    response = detectWeather(location['Latitude'], location['Longitude'])

    keyWords = parseKeyWords(response)


    setBackground(keyWords)
