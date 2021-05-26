import requests
import pandas as pd
import datetime
import numpy as np
import itertools
import os

# import joblib
from sklearn.externals import joblib
from app.config import Config
import random

darkskykey = Config["darkskykey"]
googlekey = Config["googlekey"]


script_path = os.path.dirname(os.path.abspath(__file__ + "/../"))
accident_dataset = pd.read_csv(script_path + "/app/data/accident_data.csv")


# Load  model nad model columns
model = joblib.load(script_path + "/app/model/model.pkl")
model_columns = joblib.load(script_path + "/app/model/model_columns.pkl")


def call_google(origin, destination, googlekey):
    PARAMS = {
        "origin": origin,
        "destination": destination,
        "key": googlekey,
    }
    URL = "https://maps.googleapis.com/maps/api/directions/json"
    res = requests.get(url=URL, params=PARAMS)
    data = res.json()

    # parse json to retrieve all lat-lng
    waypoints = data["routes"][0]["legs"]

    lats = []
    longs = []
    google_count_lat_long = 0

    # find cluster of interest from google api route
    for leg in waypoints:
        for step in leg["steps"]:
            start_loc = step["start_location"]
            # print("lat: " + str(start_loc['lat']) + ", lng: " + str(start_loc['lng']))
            lats.append(start_loc["lat"])
            longs.append(start_loc["lng"])
            google_count_lat_long += 1

    lats = tuple(lats)
    longs = tuple(longs)
    # print("total waypoints: " + str(google_count_lat_long))

    return lats, longs, google_count_lat_long


def calc_distance(accident_dataset, lats, longs, google_count_lat_long):
    # load all cluster accident waypoints to check against proximity
    accident_point_counts = len(accident_dataset.index)

    # approximate radius of earth in km
    R = 6373.0
    new = accident_dataset.append(
        [accident_dataset] * (google_count_lat_long - 1), ignore_index=True
    )  # repeat data frame (9746*waypoints_count) times
    lats_r = list(
        itertools.chain.from_iterable(
            itertools.repeat(x, accident_point_counts) for x in lats
        )
    )  # repeat 9746 times
    longs_r = list(
        itertools.chain.from_iterable(
            itertools.repeat(x, accident_point_counts) for x in longs
        )
    )

    # append
    new["lat2"] = np.radians(lats_r)
    new["long2"] = np.radians(longs_r)

    # cal radiun50m
    new["lat1"] = np.radians(new["Latitude"])
    new["long1"] = np.radians(new["Longitude"])
    new["dlon"] = new["long2"] - new["long1"]
    new["dlat"] = new["lat2"] - new["lat1"]

    new["a"] = (
        np.sin(new["dlat"] / 2) ** 2
        + np.cos(new["lat1"]) * np.cos(new["lat2"]) * np.sin(new["dlon"] / 2) ** 2
    )
    new["distance"] = R * (2 * np.arctan2(np.sqrt(new["a"]), np.sqrt(1 - new["a"])))

    return new


def call_darksky(clusters, darkskykey, tm):
    # weather api call
    weather = pd.DataFrame()

    # time format for darksky API, eg 2019-04-11T23:00:00
    datetime_str = datetime.datetime.strptime(tm, "%Y-%m-%dT%H:%M").strftime(
        "%Y-%m-%dT%H:%M"
    )
    tm2 = datetime_str[0:10] + "T" + datetime_str[11:13] + ":00:00"

    for index, row in clusters.iterrows():
        lat = row["Latitude"]
        long = row["Longitude"]
        weather_url = (
            "https://api.darksky.net/forecast/"
            + darkskykey
            + "/"
            + str(lat)
            + ","
            + str(long)
            + ","
            + tm2
            + "?exclude=[currently,minutely,daily,flags]"
        )
        w_response = requests.get(weather_url)
        w_data = w_response.json()

        # put json into a dataframe
        datetime_object = datetime.datetime.strptime(tm, "%Y-%m-%dT%H:%M")
        iweather = pd.DataFrame(
            w_data["hourly"]["data"][datetime_object.hour], index=[0]
        )
        iweather["Cluster"] = row["Cluster"]
        iweather["precipAccumulation"] = 0

        weather = weather.append(iweather)

    return weather


def model_pred(new_df):

    # do prediction for current datetime for all
    prob = pd.DataFrame(model.predict_proba(new_df), columns=["No", "probability"])
    prob = prob[["probability"]]
    # merge with long lat
    output = prob.merge(
        new_df[["Latitude", "Longitude"]],
        how="outer",
        left_index=True,
        right_index=True,
    )

    # drop duplicates of same lat long (multiple accidents)
    output["Latitude"] = round(output["Latitude"], 5)
    output["Longitude"] = round(output["Longitude"], 5)
    output = output.drop_duplicates(subset=["Longitude", "Latitude"], keep="last")

    # to json
    processed_results = []
    for index, row in output.iterrows():
        lat = float(row["Latitude"])
        longi = float(row["Longitude"])
        prob = float(row["probability"])

        result = {"lat": lat, "lng": longi, "probability": prob}
        processed_results.append(result)

    print("total accident count:", len(output))

    return processed_results


def get_accidents_info(lat, lng):
    results = []

    # accidents = random.radint(30,70)
    for i in range(len(lat)):
        lats = round(random.uniform(lat[i], lat[i]), 5)
        lngs = round(random.uniform(lng[i], lng[i]), 5)
        prob = random.uniform(10, 100)
        result = {"lat": lats, "lng": lngs, "probability": prob}
        results.append(result)

    return results


def api_call(origin, destination, tm):

    # parse time
    datetime_object = datetime.datetime.strptime(tm, "%Y-%m-%dT%H:%M")

    # get route planning
    lats, longs, google_count_lat_long = call_google(origin, destination, googlekey)

    # calculate distance between past accident points and route
    dist = calc_distance(accident_dataset, lats, longs, google_count_lat_long)

    # filter for past accident points with distance <50m - route cluster
    dat = dist[dist["distance"] < 0.050][
        [
            "Longitude",
            "Latitude",
            "Day_of_Week",
            "Local_Authority_(District)",
            "1st_Road_Class",
            "1st_Road_Number",
            "Speed_limit",
            "Year",
            "Cluster",
            "Day_of_year",
            "Hour",
        ]
    ]

    # if no cluster, exit
    if google_count_lat_long <= 2:
        return print(" Hooray! No accidents predicted in your route.")

    else:
        results = get_accidents_info(lats, longs)
        final = {}
        final["accidents"] = results
        return final
