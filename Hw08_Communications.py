"""
Project:     hw08-communication.py

Description: This program obtains weather data from Wundeground and delivers
             weather information to a user via Twilio's SMS service. It also
             recommends attire based on certain weather parameters.

Name:        Gina McKeown

Date:        12/10/19

Notes:       You must intall the Twilio library and the urllib2 library
             using the SSH Terminal

             sudo pip install urllib
             sudo pip install twilio
"""

# -------------------------------------------------------------------------------

from twilio.rest import Client
import json
import urllib.request

"""
API Key: 248e1900c138965f2e6541b25d112eb9
Phone Number: 9045843989
Account SID: AC182e45ef3d90397fc7aef0814526e53b
Authorization Token: c680c8a23e7f2cb83e671c0d673c0aed
"""


class Communication:
    def __init__(self):
        """
        sends a text message giving weather details and clothing recommendations for a given zip code
        """
        self.temp = ""
        self.weather = ""
        self.city = ""
        self.wind_speed = ""
        self.temp_min = ""
        self.temp_max = ""
        self.twilio_phone_num = "+19045843989"  # texts sent from this number
        self.api_key = "248e1900c138965f2e6541b25d112eb9"  # OpenWeatherMap API
        self.account_sid = "AC182e45ef3d90397fc7aef0814526e53b"  # OpenWeatherMap SID
        self.token = "c680c8a23e7f2cb83e671c0d673c0aed"  # OpenWeatherMap token

    def get_weather(self, zipcode):
        """
        returns the temperature and details about the weather for a given zip code by putting them into a string
        :param zipcode: the zip code of location user wants info on
        :return: a string with the temperature and weather of the city
        """
        url = "http://api.openweathermap.org/data/2.5/weather?zip=" + zipcode + "&APPID=" + self.api_key
        opened_url = urllib.request.urlopen(url)
        url_info = opened_url.read()
        parsed_url_info = json.loads(url_info)
        self.city = parsed_url_info["name"]
        self.temp = self.kelvin_to_fahrenheit(int(parsed_url_info["main"]["temp"]))
        self.weather = parsed_url_info["weather"][0]["description"]

        # EXTRA CREDIT
        self.wind_speed = parsed_url_info["wind"]["speed"]
        self.temp_min = self.kelvin_to_fahrenheit(int(parsed_url_info["main"]["temp_min"]))
        self.temp_max = self.kelvin_to_fahrenheit(int(parsed_url_info["main"]["temp_max"]))

        message = "Current temperature in %s is: %.1f° F\nLowest Temperature: %.1f° F\nHighest Temperature: %.1f° F" \
                  "\nWind Speed: %s\nDetails: %s" \
                  % (self.city, self.temp, self.temp_min, self.temp_max, self.wind_speed, self.weather)
        opened_url.close()
        return message

    def kelvin_to_fahrenheit(self, deg_kelvin):
        """
        takes in Kelvin and converts to degrees in Fahrenheit
        :param deg_kelvin: represents Kelvin to be converted to F
        :return: the degrees in Fahrenheit for the given Kelvin
        """
        deg_fahrenheit = (int(deg_kelvin) - 273.15) * 9 / 5 + 32  # change to fahrenheit using formula
        return deg_fahrenheit  # return the converted value

    def send_sms(self, phone_num, message):
        """
        This function sends a message to the given recipient. The message contains the given message
        and the recommended clothing for
        :param phone_num: phone number of recipient
        :param message: a message to send to recipient
        :return: a boolean for weather or not the message sent successfully
        """
        client = Client(self.account_sid, self.token)  # Create an client object
        try:
            client.api.account.messages.create(
                body=message + self.create_message(),
                to=phone_num,  # Destination phone number
                from_=self.twilio_phone_num
            )
        except:
            print("There was an error sending your message")
            return False
        return True

    def create_message(self):
        """
        creates a recommendation for clothing based on the weather conditions
        :return: a string with the clothing recommendation
        """
        message = "\nRecommendations:"
        # If its raining wear a raincoat and if its raining hard bring an umbrella too
        if self.weather.find("rain"):
            message += "\nYou should wear a raincoat!"
            if self.weather.find("extreme") or self.weather.find("heavy"):
                message += "\nRemember to bring an umbrella! :)"
        # otherwise, if its clear and under 50, bring a warm coat
        elif int(self.temp) < 50 and self.weather.find("clear"):
            message += "\nYou should wear a warm coat."
        elif self.weather.find("snow"):
            message += "\nYou might want to wear snow boots"
        if int(self.temp) < 32:
            message += "\nIt's very cold! Remember mittens and a scarf."

        # EXTRA CREDIT
        # if it's cold and windy...
        if int(self.wind_speed) > 25 and int(self.temp) < 50:
            message += "\nIt's very windy, bring a scarf and hat."
            if int(self.temp) < 32: # if it's very cold
                message += "\nIt's also very cold, bundle up!"
        # else if its less windy...
        elif int(self.wind_speed) > 10 and int(self.temp) < 50:
            message += "\nIt's breezy, bring a hat."

        # if the lowest temperature is 10 degrees lower than the current temp...
        if int(self.temp) - int(self.temp_min) > 10:
            message += "\nIt might get colder later, bring an extra sweater in case."
        return message


if __name__ == "__main__":
    com = Communication()  # create an instance of the communication class
    # CHECKING PROGRESS
    print(com.get_weather("10128"))
    com.send_sms("9292455707", "Hello")


    # Text weather info and recommendations
    zipcode = input("Enter the zip code of the location you want information on: ")  # user can choose location
    com.send_sms("9292455707", com.get_weather(zipcode))  # create a text message by getting the weather
