#! python3.10
# weather forcast
# should get your own OpenWeatherMap API key and insert it into the API url in the specified place.

import json, requests, sys, datetime
import send_auto_email_module

def confirm_command():

    if len(sys.argv) >= 3 and sys.argv[1] == 'package':
        print(f'Weather package for your customized selection of cities: --(Please wait for API response.)')
        text = ''
        for argv in sys.argv[2:]:
            try:
                print(f'\nWeather for {str(argv).title()}: --(Please wait for API response.)')
                lat,lon = get_coor(argv)
                text_curr, four_days_list = get_weather(lat, lon)
                text += f'{text_curr}\n--------------------\n{four_days_list}\n=========================\n'
            except Exception as err:
                print("Wrong location name or can't find input location. If confirm no mistake, please try again.\n")
                continue
        weather_mail(text)


    elif len(sys.argv) >= 2 and sys.argv[1] != 'package':
        location = ' '.join(sys.argv[1:])
        try:
            print(f'Weather for {location.title()}: --(Please wait for API response.)')
            lat, lon = get_coor(location)
            text_curr, four_days_list = get_weather(lat, lon)
            text = f'{text_curr}\n--------------------\n{four_days_list}\n========================='
            weather_mail(text)
        except Exception as err:
            print("Wrong location name or can't find input location. If confirm no mistake, please try again.\n")

def get_coor(location):
    formatted_loc = location.title()
    url = \
        f'http://api.openweathermap.org/geo/1.0/direct?q={formatted_loc}&limit=1&appid={API key}'# use API key here

    response = requests.get(url)
    response.raise_for_status()
    data = json.loads(response.text)
    lat_raw, lon_raw = data[0]['lat'], data[0]['lon']
    lat_f, lon_f = float(lat_raw), float(lon_raw)
    lat, lon = str(round(lat_f,2)), str(round(lon_f,2))
    return lat, lon

def get_weather(lat, lon):
    url_current = \
        f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API key}' # use API key here
    url_4days = \
        f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={API key}' # use API key here
    response_curr = requests.get(url_current)
    response_4days = requests.get(url_4days)
    response_curr.raise_for_status()
    response_4days.raise_for_status()
    data_curr, data_4days = json.loads(response_curr.text), json.loads(response_4days.text)
    now = datetime.datetime.now()
    now_time = now.strftime("%Y-%m-%d %H:%M:%S")

    text_curr = f'{now_time} \nCurrent Weather: \n\t{data_curr["weather"][0]["description"]}\n' \
                f'\t{data_curr["main"]["temp_min"]}℃ - {data_curr["main"]["temp_max"]}℃\n' \
                f'\tHumidity: {data_curr["main"]["humidity"]}%\n\tWind: {data_curr["wind"]["speed"]} m/sec\n'

    print(text_curr)
    date_stamp = [8,16,24,32]

    print('\nNext 4 Days:\n')
    four_days_list = []
    for i in date_stamp:
        text_4days = f'{data_4days["list"][i]["dt_txt"]}: {data_4days["list"][i]["weather"][0]["description"]} | ' \
                     f'{data_4days["list"][i]["main"]["temp_min"]}℃ - {data_4days["list"][i]["main"]["temp_max"]}℃ | ' \
                     f'Wind Speed: {data_4days["list"][i]["wind"]["speed"]} m/sec | ' \
                     f'Humidity: {data_4days["list"][i]["main"]["humidity"]}%'

        print(text_4days)
        print('------------------------------------------------')
        four_days_list.append(text_4days)
    print('====================================================')
    return text_curr, four_days_list

def message():
    print('Weather for any city, cmd input "weather (city)";\n'
          'Get customized weather package, cmd input "weather package (city1) (city2)...(city[n])".')
    print('====================================================')

def weather_mail(text):
    send_mail = input('Do you also want this sent to your email? "y" for yes.')
    if send_mail == 'y':
        send_auto_email_module.get_server_and_send_auto(text)

if __name__ == '__main__':
    message()
    confirm_command()
