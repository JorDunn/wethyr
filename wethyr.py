# -*- coding: utf-8 -*-
#!/usr/bin/env python

from flask import *
import json, requests, dis, operator, time

app = Flask(__name__)

app.debug = True

class Wethyr(object):

	def degreesToCardinal(self, deg):
		if(((operator.gt(deg, 326)) and (operator.lt(deg, 360))) or ((operator.gt(deg, 0)) and (operator.lt(deg, 12)))):
			return 'North'
		elif((operator.gt(deg, 11)) and (operator.lt(deg, 57))):
			return 'Northeast'
		elif((operator.gt(deg, 56)) and (operator.lt(deg, 102))):
			return 'East'
		elif((operator.gt(deg, 101)) and (operator.lt(deg, 169))):
			return 'Southeast'
		elif((operator.gt(deg, 168)) and (operator.lt(deg, 192))):
			return 'South'
		elif((operator.gt(deg, '191')) and (operator.lt(deg, 237))):
			return 'Southwest'
		elif((operator.gt(deg, 236)) and (operator.lt(deg, 282))):
			return 'West'
		elif((operator.gt(deg, 281)) and (operator.lt(deg, 327))):
			return 'Northwest'
		else:
			return 'Unknown'

	def processWeatherInfo(self, weather_json, units):
		self.weather = { 'temp': int(weather_json['main']['temp']),
						 'humidity': weather_json['main']['humidity'],
						 'pressure': weather_json['main']['pressure'],
						 'wind_speed': weather_json['wind']['speed'],
						 'wind_direction': self.degreesToCardinal(weather_json['wind']['deg']), 
						 'sky': str(weather_json['weather'][0]['main']).lower(), 
						 'sky_desc': str(weather_json['weather'][0]['description']).title(), 
						 'city': str(weather_json['name']).title(), 
						 'country': str(weather_json['sys']['country']).title(),
		}

		return self.weather

@app.route('/', methods=['GET', 'POST'])
def getWeatherDefault(city='Shakopee', country='US', units='imperial'):
	if (request.method == 'POST'):
		return redirect('/' + request.form['city'] + '/' + request.form['country'] + '/' + request.form['units'])
	else:
		url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + ',' + country + '&units=' + units

		res = requests.get(url)
		weather_json = json.loads(json.dumps(res.json()))

		wethyr = Wethyr()
		weather = wethyr.processWeatherInfo(weather_json, units)

		if (units == 'imperial'):
			flag = 'F'
		else:
			flag = 'C'

		sky = weather['sky']
		if (weather['sky'] == 'clear'):
			if ((int(time.time()) > int(weather_json['sys']['sunrise'])) and (int(time.time() < int(weather_json['sys']['sunset'])))):
				sky = 'clear_day'
			else:
				sky = 'clear_night'

		return render_template('index.html', city=weather['city'], country=weather['country'], temp=weather['temp'], humidity=weather['humidity'], pressure=weather['pressure'], wind_speed=weather['wind_speed'], wind_direction=weather['wind_direction'], sky=sky, sky_desc=weather['sky_desc'], flag=flag)

@app.route('/<city>/<country>/<units>', methods=['GET'])
def getWeatherByCity(city='Shakopee', country='US', units='imperial'):
	url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + ',' + country + '&units=' + units

	res = requests.get(url)
	weather_json = json.loads(json.dumps(res.json()))

	wethyr = Wethyr()
	weather = wethyr.processWeatherInfo(weather_json, units)

	if (units == 'imperial'):
		flag = 'F'
	else:
		flag = 'C'

	sky = weather['sky']
	if (weather['sky'] == 'clear'):
		if ((int(time.time()) > int(weather_json['sys']['sunrise'])) and (int(time.time() < int(weather_json['sys']['sunset'])))):
			sky = 'clear_day'
		else:
			sky = 'clear_night'

	return render_template('index.html', city=weather['city'], country=weather['country'], temp=weather['temp'], humidity=weather['humidity'], pressure=weather['pressure'], wind_speed=weather['wind_speed'], wind_direction=weather['wind_direction'], sky=sky, sky_desc=weather['sky_desc'], flag=flag)

@app.route('/lat/<lat>/lon/<lon>/<units>', methods=['GET'])
def getWeatherByCoords(lat, lon, units='imperial'):
	url = 'http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lon + '&units=' + units

	res = requests.get(url)
	weather_json = json.loads(json.dumps(res.json()))

	wethyr = Wethyr()
	weather = wethyr.processWeatherInfo(weather_json, units)

	if (units == 'imperial'):
		flag = 'F'
	else:
		flag = 'C'

	sky = weather['sky']
	if (weather['sky'] == 'clear'):
		if ((int(time.time()) > int(weather_json['sys']['sunrise'])) and (int(time.time() < int(weather_json['sys']['sunset'])))):
			sky = 'clear_day'
		else:
			sky = 'clear_night'

	return render_template('index.html', city=weather['city'], country=weather['country'], temp=weather['temp'], humidity=weather['humidity'], pressure=weather['pressure'], wind_speed=weather['wind_speed'], wind_direction=weather['wind_direction'], sky=sky, sky_desc=weather['sky_desc'], flag=flag)

@app.route('/coords')
def getCoords():
	return render_template('coords.html')

if __name__ == '__main__':
	app.run()
