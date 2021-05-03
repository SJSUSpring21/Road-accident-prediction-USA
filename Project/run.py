from flask import Flask, render_template, request
import requests
import pickle
import configparser
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import pytz
from sklearn import preprocessing
from sklearn.externals import joblib


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = 0
    latitude = 9.9312
    longitude = 76.2673
    api_key = get_api_key()
    data = get_weather_results(latitude, longitude, api_key)
    print(data)
    # temperature = "{0:.2f}".format(data["main"]["temp"])
    temperature = data["main"]["temp"]
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    visibility = data["visibility"]
    precipitation = data["clouds"]["all"]
    windspeed = data["wind"]["speed"]
    timezone = int(data["timezone"])
    dtt = datetime.utcnow() + timedelta(seconds=timezone)
    year = dtt.year
    month = dtt.month
    day = dtt.day
    minute = dtt.minute
    hour = dtt.hour
    weekday = dtt.weekday()
    features = [
        latitude,
        longitude,
        temperature,
        humidity,
        pressure,
        visibility,
        windspeed,
        precipitation,
        year,
        month,
        weekday,
        day,
        hour,
        minute,
    ]
    features = np.array(features)
    print(features)
    scaler_filename = "saved_scaler"
    scaler = joblib.load(scaler_filename)
    features_transform = scaler.transform([features])
    print(features_transform)
    model = pickle.load(open("lr_model.pkl", "rb"))

    prediction = model.predict(features_transform)

    print(prediction)

    return render_template("index.html", prediction=prediction)


def get_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["openweathermap"]["api"]


def get_weather_results(latitude, longitude, api_key):
    api_url = (
        "http://api.openweathermap.org/"
        "data/2.5/weather?lat={}&lon={}&units=imperial&appid={}".format(
            latitude, longitude, api_key
        )
    )
    r = requests.get(api_url)
    return r.json()


if __name__ == "__main__":
    app.run(debug=True)
