import tkinter as tk
from tkinter import messagebox
import requests

# OpenWeatherMap API settings
API_KEY = 'apiKey'  # Replace with your OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Function to get a city's weather
def get_weather(city):
    """
    Fetch weather data for the given city using OpenWeatherMap API.
    """
    try:
        # Make API request
        params = {"q": city, "appid": API_KEY, "units": "metric"}  # Use "imperial" for Fahrenheit
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        print(data)

        # Check if the city was found
        if data["cod"] != 200:
            messagebox.showerror("Error", data["message"])
            return None

        # Extract relevant weather data
        weather = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
        }
        return weather
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None
        
# To display results of city weather
def display_weather():
    """
        Fetch and display weather data for the entered city.
    """
    city = entry.get()
    if not city:
        # To make it more precise put the city's name, comma, 2-letter country code (ISO3166).
        # You will get all proper cities in chosen country.
        # The order is important - the first is city name then comma then country. Example - London, GB or New York, US. 
        messagebox.showwarning("Input Error", "Please enter a  city name then comma then country.")
        return

    weather = get_weather(city)
    if weather:
        # Update the labels with weather data
        city_label.config(text=f"Weather in {weather['city']}")
        temp_label.config(text=f"Temperature: {weather['temperature']}°C")
        humidity_label.config(text=f"Humidity: {weather['humidity']}%")
        desc_label.config(text=f"Description: {weather['description'].capitalize()}")

        # Display weather icon (optional)
        icon_url = f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png"
        icon_data = requests.get(icon_url, stream=True).raw
        icon_image = tk.PhotoImage(data=icon_data.read())
        icon_label.config(image=icon_image)
        icon_label.image = icon_image  # Keep a reference to avoid garbage collection
        
# Function to clear entry box
def clear_entry():
    # Clear the content of the entry widget
    entry.delete(0, tk.END)
    
    # Clearing label text
    city_label.config(text="")
    temp_label.config(text="")
    humidity_label.config(text="")
    desc_label.config(text="")
    icon_label.image = None
    icon_label.config(image=None)  # Clear the icon if using an image    
    
# Create the main window
root = tk.Tk()
root.title("Real-Time Weather App")

# Center the root window
# Set the initial size of the window
x = 700  # Width of the window
y = 400  # Height of the window
root.geometry(f'{x}x{y}')  # Set the window size

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the new position to center the window
new_x = int((screen_width / 2) - (x / 2))
new_y = int((screen_height / 2) - (y / 2))

# Set the window position
root.geometry(f'{x}x{y}+{new_x}+{new_y}')

# Create and place widgets
label = tk.Label(root, text="Enter City name then comma then country:")
label.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

button = tk.Button(root, text="Get Weather", command=display_weather)
button.pack(pady=10)

button = tk.Button(root, text="Clear Entry and display", command=clear_entry)
button.pack(pady=10)


city_label = tk.Label(root, text="", font=("Arial", 16))
city_label.pack(pady=10)

temp_label = tk.Label(root, text="")
temp_label.pack()

humidity_label = tk.Label(root, text="")
humidity_label.pack()

desc_label = tk.Label(root, text="")
desc_label.pack()

icon_label = tk.Label(root)
icon_label.pack()

# Run the application
root.mainloop()
