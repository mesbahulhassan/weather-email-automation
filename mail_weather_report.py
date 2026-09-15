import requests
import json
import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
from datetime import datetime

try:
    latitude = float(input('input the latitude: '))
    longitude = float(input('input the longitude: '))

    try:
        url = 'https://api.open-meteo.com/v1/forecast'

        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m',
            'timezone': 'Asia/Dhaka'

        }
        response = requests.get(url, params= params)
        response.raise_for_status()

        data = response.json()

        with open('new_weather.json', 'w') as file:
            json.dump(data, file, indent = 4)

        weather_descriptions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
            }

        current = data['current']
        time = current['time']
        formated_time = datetime.fromisoformat(time).strftime("%d %B %Y, %I:%M %p")
        temperature = current['temperature_2m']
        feels_like = current['apparent_temperature']
        humidity = current['relative_humidity_2m']
        precipitation_probability = current['precipitation_probability']
        wind_speed = current['wind_speed_10m']
        description = weather_descriptions.get(current['weather_code'], 'unknown weather')


        weather_email_body = f"""

Weather Report
        
Latitude: {latitude}
Longitude: {longitude}
        
Weather

Time: {formated_time}
Temperature: {temperature}\u00b0C
Feels Like Temperature: {feels_like}\u00b0C
Relative Humidity: {humidity}%
Precipation Probability: {precipitation_probability}%
Wind Speed: {wind_speed}km/h
Weather Description: {description}




        """
        print(weather_email_body)


        load_dotenv()

        sender_email = os.getenv('sender_email')
        reciver_email = os.getenv('reciver_email')
        email_password = os.getenv('email_password')
        

        message = EmailMessage()
        message['Subject'] = 'Weather Report'
        message['From'] = sender_email
        message['To'] = reciver_email

        message.set_content(weather_email_body)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, email_password)
            server.send_message(message)
        

    except requests.exceptions.HTTPError as err:
        print(f'Type the right url: {err}')

    except requests.exceptions.ConnectTimeout as err:
        print(f'connectiong taking longer time than expected: {err}')

except ValueError as err:
    print(f'type the right value: {err}')
