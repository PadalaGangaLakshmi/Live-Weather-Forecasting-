from flask import Flask, render_template, request
import requests
from datetime import datetime

# import MongoClient to connect to MongoDB
from pymongo import MongoClient

app = Flask(__name__)

# define your API key
api_key = "98632acd03acc535ab8423f6792f24d3"

# connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['weather_forecast']
collection = db['forecasts']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        location = request.form['location']
        url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            forecast = f'The current temperature is {temp}°C with {weather}. Humidity is {humidity}%. Wind speed is {wind_speed} m/s.'
            # add the forecast to the MongoDB collection
            collection.insert_one({'location': location, 'forecast': forecast, 'date_time': date_time})
            return render_template('index.html', forecast=forecast, location=location)
        else:
            forecast = 'Unable to retrieve weather forecast.'
            return render_template('index.html', forecast=forecast)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)