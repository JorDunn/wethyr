# -*- coding: utf-8 -*-
#!/usr/bin/env python

from flask import *
import json, requests, dis, operator

app = Flask(__name__)

app.debug = True

def windCardinal(deg):
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

@app.route('/', methods=['GET', 'POST'])
def index(city='Shakopee', country='US', units='imperial'):
	if (request.method == 'POST'):
		return redirect('/' + request.form['city'] + '/' + request.form['country'] + '/' + request.form['units'])
	else:
		url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + ',' + country + '&units=' + units

		res = requests.get(url)
		weather = json.loads(json.dumps(res.json()))

		temp     = int(weather['main']['temp'])
		temp_hi  = weather['main']['temp_max']
		temp_low = weather['main']['temp_min']

		humidity = weather['main']['humidity']
		pressure = weather['main']['pressure']

		wind_speed = weather['wind']['speed']
		wind_direction = windCardinal(weather['wind']['deg'])

		sky      = weather['weather'][0]['main']
		sky_desc = weather['weather'][0]['description']
		sky_desc = sky_desc.title()

		if(units == 'imperial'):
			flag = 'F'
		else:
			flag = 'C'

		return render_template('index.html', city=city, country=country, temp=temp, temp_hi=temp_hi, temp_low=temp_low, humidity=humidity, pressure=pressure, wind_speed=wind_speed, wind_direction=wind_direction, sky=sky, sky_desc=sky_desc, flag=flag)

@app.route('/<city>/<country>/<units>', methods=['GET'])
def getWeather(city='Shakopee', country='US', units='imperial'):
	url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + ',' + country + '&units=' + units

	res = requests.get(url)
	weather = json.loads(json.dumps(res.json()))

	temp     = int(weather['main']['temp'])
	temp_hi  = weather['main']['temp_max']
	temp_low = weather['main']['temp_min']

	humidity = weather['main']['humidity']
	pressure = weather['main']['pressure']

	wind_speed = weather['wind']['speed']
	wind_direction = windCardinal(weather['wind']['deg'])

	sky      = weather['weather'][0]['main']
	sky_desc = weather['weather'][0]['description']

	if(units == 'imperial'):
		flag = 'F'
	else:
		flag = 'C'

	return render_template('index.html', city=city, country=country, temp=temp, temp_hi=temp_hi, temp_low=temp_low, humidity=humidity, pressure=pressure, wind_speed=wind_speed, wind_direction=wind_direction, sky=sky, sky_desc=sky_desc, flag=flag)

if __name__ == '__main__':
	app.run()