import requests

def get_weather(api_key, location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def display_weather(data):
    if data is None:
        return
    
    if data.get("cod") == "404":
        print("City not found. Please check your input.")
    elif data.get("cod") == "401":
        print("Unauthorized: Please check your API key.")
    else:
        city = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "Unknown")
        weather_desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        print(f"Weather in {city} ({country}):")
        print(f"Description: {weather_desc}")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")

if __name__ == "__main__":
    api_key = "0f2da766b4d61c386ec2f19799de2975"
    location = input("Enter city name or ZIP code: ")
    
    weather_data = get_weather(api_key, location)
    display_weather(weather_data)
