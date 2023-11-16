import tkinter
import customtkinter
from settings import Settings
from customtkinter import CTkImage
from PIL import Image, ImageTk

from ..backend.weatherApp_API_Testing import WeatherDataFetcher




class Settings:
    def __init__(self, app) -> None:
        self.app = app

    def set_theme(self, theme):
        customtkinter.set_default_color_theme(theme)
    
    def set_appearance_mode(self, mode):
        customtkinter.set_appearance_mode(mode)

class Navigation:
    def __init__(self, app):
        self.app = app
        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        # Settings gear button
        gear_image = Image.open("src/frontend/assets/gear.png").resize((30, 30), Image.Resampling.LANCZOS)
        gear_icon = customtkinter.CTkImage(gear_image)
        self.settings_button = customtkinter.CTkButton(self.app, image=gear_icon, width=30, height=30, command=self.on_settings_click, text="")
        self.settings_button.grid(row=1, column=5, padx=10, pady=5, sticky="e")

        # Left arrow button
        left_image = Image.open("src/frontend/assets/left.png").resize((20, 20), Image.Resampling.LANCZOS)
        left_icon = customtkinter.CTkImage(left_image)
        self.left_button = customtkinter.CTkButton(self.app, image=left_icon, width=20, height=20, command=self.on_left_click, text="")
        self.left_button.grid(row=2, column=1, padx=10, pady=10)

        # Right arrow button
        right_image = Image.open("src/frontend/assets/right.png").resize((20, 20), Image.Resampling.LANCZOS)
        right_icon = customtkinter.CTkImage(right_image)
        self.right_button = customtkinter.CTkButton(self.app, image=right_icon, width=20, height=20, command=self.on_right_click, text="")
        self.right_button.grid(row=2, column=4, padx=10, pady=10)

    def on_settings_click(self):
        self.settingsframe = tkinter.Frame(self.app)
        self.settingsframe.grid(row=2, column=5, padx=10, pady=5)
        self.settings_box = Settings(self.settingsframe)
        

    def on_left_click(self):
        print("Left arrow clicked")

    def on_right_click(self):
        print("Right arrow clicked")

class Search:
    def __init__(self, app):
        self.app = app
        self.location = customtkinter.StringVar()
        self.create_search_entry()

    def create_search_entry(self):
        self.search_entry = customtkinter.CTkEntry(
            self.app, width=120, height=40, corner_radius=2, border_width=2,
            placeholder_text="Search for a Location", textvariable=self.location
        )
        self.search_entry.grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky="ew")

    def get_search_text(self):
        return self.location.get()
    
    def on_search_submit(self):
        city = self.get_search_text()
        self.app.update_city(city)


class WeatherDisplay:
    def __init__(self, app):
        self.app = app
        self.create_display_labels()

    def create_display_labels(self):
        # Temperature Label
        self.temp_label = customtkinter.CTkLabel(self.app, text="60° F", font=("Roboto", 40))
        self.temp_label.grid(row=3, column=2, padx=0, pady=10, sticky="nsew")

        # Weather Condition Label
        self.weather_label = customtkinter.CTkLabel(self.app, text="Cloudy", font=("Roboto", 30))
        self.weather_label.grid(row=3, column=3, padx=0, pady=10, sticky="nsew")

    def update_weather(self, temperature, condition):
        self.temp_label.configure(text=f"{temperature}° F")
        self.weather_label.configure(text=condition)

class Forecast:
    def __init__(self, app, data_loader, scrollable_area):
        self.app = app
        self.data_loader = data_loader
        self.scrollable_area = scrollable_area
        self.create_forecast_buttons()


    def create_forecast_buttons(self):
        self.hourly_button = customtkinter.CTkButton(
            self.app, text="Hourly", command=lambda: self.select_forecast("hourly"),
            text_color="black", border_width=1
        )
        self.hourly_button.grid(row=5, column=2, padx=0, pady=10)

        self.daily_button = customtkinter.CTkButton(
            self.app, text="Daily", command=lambda: self.select_forecast("daily"),
            text_color="black"
        )
        self.daily_button.grid(row=5, column=3, padx=0, pady=10)

    def select_forecast(self, forecast_type):
        if forecast_type == "hourly":
            self.hourly_button.configure(fg_color="#4da6ff")  # Highlighted color
            self.daily_button.configure(fg_color="#F0F0F0")   # Default color
            self.scrollable_area.update_area(self.data_loader.hourly_forecast)
        elif forecast_type == "daily":
            self.daily_button.configure(fg_color="#4da6ff")   # Highlighted color
            self.hourly_button.configure(fg_color="#F0F0F0")  # Default color
            self.scrollable_area.update_area(self.data_loader.daily_forecast)

class DataLoader:
    def __init__(self, weather_display, scrollable_area, city):
        self.weather_fetcher = WeatherDataFetcher(city)
        self.weather_display = weather_display
        self.scrollable_area = scrollable_area
        self.hourly_forecast = None
        self.daily_forecast = None

    def load_data(self):
        current_weather = self.weather_fetcher.fetch_current_weather()
        if current_weather:
            self.weather_display.update_weather(current_weather['current']['temp_c'],
                                                current_weather['current']['condition']['text'])

        self.hourly_forecast = self.weather_fetcher.fetch_hourly_forecast()
        self.scrollable_area.update_area(self.hourly_forecast)
        
        self.daily_forecast = self.weather_fetcher.fetch_daily_forecast()

    def process_forecast_data(self, data):
        # Process the raw API data to match the expected format
        return data.get('list', [])

class ScrollableArea:
    def __init__(self, app):
        self.app = app
        self.create_scrollable_area()

    def create_scrollable_area(self):
        self.forecast_container = customtkinter.CTkFrame(self.app, corner_radius=10)
        self.forecast_container.grid(row=6, column=1, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Using CTKCanvas instead of the standard Canvas
        self.forecast_canvas = customtkinter.CTkCanvas(self.forecast_container)
        self.forecast_canvas.pack(side="left", fill="both", expand=True)

        # Using CTKScrollbar instead of the standard Scrollbar
        self.scrollbar = customtkinter.CTkScrollbar(self.forecast_container, command=self.forecast_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.forecast_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.forecast_canvas.bind('<Configure>', lambda e: self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox("all")))

        self.forecast_frame = customtkinter.CTkFrame(self.forecast_canvas)
        self.forecast_canvas.create_window((0, 0), window=self.forecast_frame, anchor="nw")
    
    def update_area(self, forecast_data):
        #print("Forecast data structure:", type(forecast_data), forecast_data) # For testing
        # Clear existing forecast widgets
        for widget in self.forecast_frame.winfo_children():
            widget.destroy()

        # Iterate through the forecast data and create widgets for each entry
        for forecast in forecast_data['list']:
            # Extract data from each forecast entry
            # Adjust these lines based on the actual structure of your forecast data
            #date_time = forecast.get('dt_txt', 'N/A')
            temp = forecast['main']['temp'] - 273.15 # Convert from Kelvin to Celsius
            condition = forecast['weather'][0]['description']
            chance_of_rain = forecast.get('pop', 0) * 100  # Convert to percentage

            # Create a label for each forecast entry and add it to the scrollable frame
            label_text = f"Temp: {temp:.1f}°C, Condition: {condition}, Rain Chance: {chance_of_rain}%"
            label = customtkinter.CTkLabel(self.forecast_frame, text=label_text)
            label.pack(padx=10, pady=5, anchor='w')


class WeatherApp:
    def __init__(self):
        # Initialize the main window
        self.app = customtkinter.CTk()
        self.settings = Settings(self.app)
        self.setup_window()

        self.configure_layout()
        self.title = customtkinter.CTkLabel(self.app, text="The Weather App")
        self.title.grid(row=0, column=0, columnspan=6, padx=5, pady=5, sticky="ew")
        
        self.navigation = Navigation(self.app)
        self.search = Search(self.app)
        self.weather_display = WeatherDisplay(self.app)
        self.scrollable_area = ScrollableArea(self.app)
        self.default_city = "Corvallis"
        self.data_loader = DataLoader(self.weather_display, self.scrollable_area, self.default_city)
        self.forecast = Forecast(self.app, self.data_loader, self.scrollable_area)
    
    def update_city(self, city):
        self.data_loader.city = city
        self.data_loader.load_data()

    def setup_window(self):
        self.app.title("The Weather App")
        self.app.geometry("720x480")
        self.settings.set_appearance_mode("System")  
        self.settings.set_theme("blue")  

    def configure_layout(self):
        for i in range(6):
            self.app.grid_columnconfigure(i, weight=1)
        self.app.grid_rowconfigure(6, weight=1)
        

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    weather_app = WeatherApp()
    weather_app.update_city(weather_app.default_city)
    weather_app.run()