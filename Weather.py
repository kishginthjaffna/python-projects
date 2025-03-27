import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from requests import HTTPError


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.city_label = QLabel("Enter city name ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature = QLabel(self)
        self.emoji_label = QLabel(self)
        self.desc = QLabel(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 200, 400)

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.desc)

        self.setLayout(vbox)

        self.city_label.setAlignment((Qt.AlignCenter))
        self.city_input.setAlignment((Qt.AlignCenter))
        self.temperature.setAlignment((Qt.AlignCenter))
        self.emoji_label.setAlignment((Qt.AlignCenter))
        self.desc.setAlignment((Qt.AlignCenter))

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature.setObjectName("temperature")
        self.emoji_label.setObjectName("emoji_label")
        self.desc.setObjectName("desc")

        self.setStyleSheet("""
            QLabel{
                font-family: Arial;
                font-size: 40px;
                margin: 0px 20px;
            }
            QPushButton, QLineEdit{
                font-family: Arial;
                font-size: 20px;
                padding: 10px 20px;
            }
            QLabel#city_label{
                font-style: italic;
            }
            QPushButton#get_weather_button{
                font-weight: bold;
            }
            QLabel#emoji_label{
                font-family: Segoe UI emoji;
            }
        """)

        self.get_weather_button.clicked.connect(self.getWeather)

    def getWeather(self):
        api_key = "1a36dfec5045c2749952ccded792b4da"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()

            if data["cod"] == 200:
                self.displayWeather(data)

        except requests.exceptions.HTTPError as httpError:
            match res.status_code:
                case 400:
                    self.displayError("Bad Request!")
                case 401:
                    self.displayError("Unauthorized user!")
                case 403:
                    self.displayError("Access Denied!")
                case 404:
                    self.displayError("Not Found!")
                case 500:
                    self.displayError("Internal Server Error!")
                case 502:
                    self.displayError("Bad Gateway!")
                case 503:
                    self.displayError("Service unavailable!")
                case 504:
                    self.displayError("Gateway Timeout!")
                case _:
                    self.displayError(httpError)

        except requests.exceptions.ConnectionError:
            self.displayError("Connection Error! CHeck your internet connection!")
        except requests.exceptions.Timeout:
            self.displayError("Request Time Out!")

        except requests.exceptions.TooManyRedirects:
            self.displayError("Too many redirects!")

        except requests.exceptions.RequestException as reqError:
            self.displayError(reqError)





    def displayError(self, message):
        self.temperature.setText(message)

    def displayWeather(self, data):
        temp_kelvin = data["main"]["temp"]
        temp_celsius = round(temp_kelvin - 273.15, 2)
        description = data["weather"][0]["description"].capitalize()

        weather_id = data["weather"][0]["id"]
        emoji = self.getWeatherEmoji(weather_id)

        self.temperature.setText(f"{temp_celsius}°C")
        self.desc.setText(description)
        self.emoji_label.setText(emoji)

    def getWeatherEmoji(self, weather_id):
        if 200 <= weather_id < 300:
            return "⛈️"  # Thunderstorm
        elif 300 <= weather_id < 400:
            return "🌧️"  # Drizzle
        elif 500 <= weather_id < 600:
            return "🌦️"  # Rain
        elif 600 <= weather_id < 700:
            return "❄️"  # Snow
        elif 700 <= weather_id < 800:
            return "🌫️"  # Atmosphere (Fog, Smoke, etc.)
        elif weather_id == 800:
            return "☀️"  # Clear
        elif 801 <= weather_id < 810:
            return "⛅"  # Cloudy
        else:
            return "🌍"  # Default


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
