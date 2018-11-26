# -*- coding: utf-8 -*-
from random import randint, uniform
import requests
from flask import Flask, render_template
from pprint import pprint
from mongoengine import *
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

token = ""
app = Flask(__name__)

class Post(Document):
    data = DictField(required=True)
    status = StringField(required=True)

def getNewData():
    print("Fetching new data from the API")
    r = requests.get('http://api.waqi.info/feed/delhi/?token=088a245760a1d4e479758249087ad11a11cd6221')
    # r.encoding = 'ISO-8859-1'
    data = r.json()
    time_values = []
    for time in Post.objects:
        time_values.append(time['data']['time']['v'])

    if r.json()['data']['time']['v'] not in time_values:
        print("Obtained new data point, adding it to database")
        post_1 = Post(data=r.json()['data'], status=r.json()['status'])
        post_1.save()

@app.route('/data')
def data():
    # http://api.waqi.info/feed/delhi/?token=088a245760a1d4e479758249087ad11a11cd6221
    data = []
    for data_point in Post.objects:
        data.append(data_point['data'])
    return render_template('data.html', data=data)

@app.route('/')
def index():
    temp_values = []
    aqi_values = []
    for data_point in Post.objects:
        time = data_point['data']['time']['s']
        temp = data_point['data']['iaqi']['t']['v']
        aqi = data_point['data']['aqi']
        temp_values.append({'x': time, 'y': temp})
        aqi_values.append({'x': time, 'y': aqi})
    print(temp_values, aqi_values)
    return render_template('index.html', temp_values=temp_values, aqi_values=aqi_values)

if __name__ == "__main__":
    # Make connection to MongoDB
    connect('Climate_database', host='localhost', port=27018)
    getNewData()
    scheduler = BackgroundScheduler()
    scheduler.add_job(getNewData, 'interval', seconds=900)
    # scheduler.add()
    scheduler.start()
    try:
        app.run(host='0.0.0.0', port=5000, use_reloader=True, threaded=True)
    except (KeyboardInterrupt, SystemExit):
        print("Stopping the application. Database will no longer be updated!")
        scheduler.shutdown()
