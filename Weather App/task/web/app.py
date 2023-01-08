import datetime

from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import requests
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.secret_key = "kekus"
db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


def get_weather(city, id):
    r = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid=c636a96edf9180909ce461b782db1eb6")
    lat = r.json()[0]["lat"]
    lon = r.json()[0]["lon"]
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric"
                     f"&appid=c636a96edf9180909ce461b782db1eb6")
    local_time = (datetime.datetime.utcnow() + datetime.timedelta(seconds=r.json()['timezone'])).strftime("%H")

    day_state = None

    if 6 <= int(local_time) <= 16:
        day_state = 'day'
    elif 17 <= int(local_time) <= 23:
        day_state = 'evening-morning'
    elif 0 <= int(local_time) <= 5:
        day_state = 'night'

    weather = {
        "id": id,
        "degree": r.json()["main"]["temp"],
        "state": r.json()["weather"][0]["main"],
        "city": city,
        "day_state": day_state
    }
    return weather


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    cities = City.query.all()
    weather = []
    for city in cities:
        weather.append(get_weather(city.name, city.id))

    return render_template("index.html", weather=weather)


@app.route('/add', methods=['POST'])
def add_city():
    city = request.form['city_name']
    r = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid=c636a96edf9180909ce461b782db1eb6")

    if not r.json():
        flash("The city doesn't exist!")
        return redirect("/")

    if City.query.filter_by(name=city).first():
        flash("The city has already been added to the list!")
        return redirect("/")

    db.session.add(City(name=city))
    db.session.commit()
    return redirect("/")


@app.route('/delete/<city_id>', methods=['GET', 'POST'])
def delete(city_id):
    city = City.query.filter_by(id=city_id).first()
    db.session.delete(city)
    db.session.commit()
    return redirect('/')


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(debug=True)
