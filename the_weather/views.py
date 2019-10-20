import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
import datetime


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == '200':

                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'
            else:
                err_msg = 'City already exists in the database!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        d1 = int(r['list'][0]['dt'])
        d2 = int(r['list'][8]['dt'])
        d3 = int(r['list'][16]['dt'])
        d4 = int(r['list'][24]['dt'])
        d5 = int(r['list'][32]['dt'])

        days = [datetime.datetime.utcfromtimestamp(d1).isoweekday(), datetime.datetime.utcfromtimestamp(d2).isoweekday(),
                datetime.datetime.utcfromtimestamp(d3).isoweekday(), datetime.datetime.utcfromtimestamp(d4).isoweekday(),
                datetime.datetime.utcfromtimestamp(d5).isoweekday()]
        for day in range(0, 5):

            if days[day] == 1:
                days[day] = 'Monday'

            if days[day] == 2:
                days[day] = 'Tuesday'

            if days[day] == 3:
                days[day] = 'Wednesday'

            if days[day] == 4:
                days[day] = 'Thursday'

            if days[day] == 5:
                days[day] = 'Friday'

            if days[day] == 6:
                days[day] = 'Saturday'

            if days[day] == 7:
                days[day] = 'Sunday'



        city_weather = {
            'city': city.name,
            'd1': days[0],
            'd1temperature': r['list'][0]['main']['temp'],
            'd1description': r['list'][0]['weather'][0]['description'],
            'd1icon': r['list'][0]['weather'][0]['icon'],

            'd2': days[1],
            'd2temperature': r['list'][8]['main']['temp'],
            'd2description': r['list'][8]['weather'][0]['description'],
            'd2icon': r['list'][8]['weather'][0]['icon'],

            'd3': days[2],
            'd3temperature': r['list'][16]['main']['temp'],
            'd3description': r['list'][16]['weather'][0]['description'],
            'd3icon': r['list'][16]['weather'][0]['icon'],

            'd4': days[3],
            'd4temperature': r['list'][24]['main']['temp'],
            'd4description': r['list'][24]['weather'][0]['description'],
            'd4icon': r['list'][24]['weather'][0]['icon'],

            'd5': days[4],
            'd5temperature': r['list'][32]['main']['temp'],
            'd5description': r['list'][32]['weather'][0]['description'],
            'd5icon': r['list'][32]['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class
    }

    return render(request, 'the_weather/the_weather.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect('home')