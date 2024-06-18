import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Weather App')
        self.setGeometry(100, 100, 800, 600)

        self.api_key = '0f2da766b4d61c386ec2f19799de2975'  # OpenWeatherMap API key

        self.location_label = QLabel('Enter city name or ZIP code:')
        self.location_input = QLineEdit()
        self.fetch_button = QPushButton('Fetch Weather')
        self.fetch_button.clicked.connect(self.fetch_weather)

        self.current_weather_label = QLabel()
        self.weather_icon_label = QLabel()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.location_label)
        self.layout.addWidget(self.location_input)
        self.layout.addWidget(self.fetch_button)
        self.layout.addWidget(self.current_weather_label)
        self.layout.addWidget(self.weather_icon_label)

        self.setLayout(self.layout)

    def fetch_weather(self):
        location = self.location_input.text()
        if not location:
            QMessageBox.warning(self, 'Warning', 'Please enter a location.')
            return

        weather_data = self.get_weather(location, 'metric')  # Use metric units (Celsius)

        if weather_data:
            self.display_weather(weather_data)
        else:
            QMessageBox.critical(self, 'Error', 'Failed to fetch weather data.')

    def get_weather(self, location, units):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}&units={units}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def display_weather(self, data):
        if data.get('cod') == '404':
            QMessageBox.warning(self, 'Warning', 'City not found. Please check your input.')
            return
        
        city = data.get('name', 'Unknown')
        country = data.get('sys', {}).get('country', 'Unknown')
        weather_desc = data['weather'][0]['description'].capitalize()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        icon_id = data['weather'][0]['icon']

        self.current_weather_label.setText(f"Weather in {city} ({country}):\n"
                                           f"Description: {weather_desc}\n"
                                           f"Temperature: {temp}°C\n"
                                           f"Humidity: {humidity}%")

        icon_url = f"http://openweathermap.org/img/wn/{icon_id}.png"
        icon_data = requests.get(icon_url).content
        pixmap = QPixmap()
        pixmap.loadFromData(icon_data)
        self.weather_icon_label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
