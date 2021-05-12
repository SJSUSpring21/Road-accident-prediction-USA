from flask import render_template, request, Blueprint, jsonify
from app.api_call_pred import api_call
import datetime
import json
import traceback

main = Blueprint('main', __name__)

# home page
@main.route("/")
@main.route("/home")
def home():
    return render_template('index.html')

@main.route("/exploration")
def exploration():
    return render_template('exploration.html')

@main.route("/register")
def register():
    return render_template('register.html')

@main.route("/login")
def login():
    return render_template('login.html')

@main.route("/interaction")
def interaction():
    return render_template('interaction.html')


@main.route("/days")
def days():
    return render_template('days.html')


@main.route("/city")
def city():
    return render_template('city.html')

@main.route("/weather_info")
def weather_info():
    return render_template('weather.html')

@main.route("/map")
def map():
    return render_template('predictionmap.html')

#API to get user inputs
@main.route('/prediction', methods=['GET','POST'])
def prediction():
    req_data = request.get_json()
    print(req_data)
    origin = req_data['origin']
    destination = req_data['destination']
    date_time = req_data['datetime']

    #process time
    tm = datetime.datetime.strptime(date_time,'%Y/%m/%d %H:%M').strftime('%Y-%m-%dT%H:%M')

    out = api_call(origin, destination, tm)

    return json.dumps(out)


