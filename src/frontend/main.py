import tkinter
import customtkinter as ctk
from ..frontend.settings import Settings
from customtkinter import CTkImage
from PIL import Image, ImageTk

#from ..backend.weatherApp_API_Testing import WeatherDataFetcher
from ..backend.API import initialize
from ..backend.API import current_Location


"""
Sets up 3 icons: the left and right buttons to select different saved locations as well
as the gear icon that opens the settings menu.
"""
class Navigation:
    def __init__(self, app, data_loader):
        self.app = app
        self.data_loader = data_loader
        self.create_navigation_buttons()
        self.settings_clicked = False
        self.heart_clicked = False
        

    def create_navigation_buttons(self):
        # Settings gear button
        gear_image = Image.open("src/frontend/assets/gear.png").resize((30, 30), Image.BICUBIC)
        gear_icon = ctk.CTkImage(gear_image)
        self.settings_button = ctk.CTkButton(self.app, image=gear_icon, width=30, height=30, command=self.on_settings_click, text="")
        self.settings_button.grid(row=1, column=5, padx=10, pady=5, sticky="e")

        # Create and hide settings panel
        self.settingsframe = tkinter.Frame(self.app)
        self.settingsframe.grid(row=2, column=5, padx=10, pady=5)
        self.settings_box = Settings(self.settingsframe, self.data_loader)
        self.settingsframe.grid_remove()

        # Favorite Location Button
        heart_image = Image.open("src/frontend/assets/heart.png").resize((30, 30), Image.BICUBIC)
        heart_icon = ctk.CTkImage(heart_image)
        self.settings_button = ctk.CTkButton(self.app, image=heart_icon, width=30, height=30, command=self.on_favorite_click, text="")
        self.settings_button.grid(row=2, column=3, padx=10, pady=5, sticky="e")

        # Left arrow button
        left_image = Image.open("src/frontend/assets/left.png").resize((20, 20), Image.BICUBIC)
        left_icon = ctk.CTkImage(left_image)
        self.left_button = ctk.CTkButton(self.app, image=left_icon, width=20, height=20, command=self.on_left_click, text="")
        self.left_button.grid(row=2, column=1, padx=10, pady=10)

        # Right arrow button
        right_image = Image.open("src/frontend/assets/right.png").resize((20, 20), Image.BICUBIC)
        right_icon = ctk.CTkImage(right_image)
        self.right_button = ctk.CTkButton(self.app, image=right_icon, width=20, height=20, command=self.on_right_click, text="")
        self.right_button.grid(row=2, column=4, padx=10, pady=10)

        # Location Display Box
        self.location_box = ctk.CTkLabel(self.app, text="Corvallis", fg_color="#4da6ff", font=("Verdana", 35),
                                                    corner_radius=7, text_color="black")
        self.location_box.grid(row=2, column=2, columnspan = 2, padx=5, pady=(50, 15))

    def on_settings_click(self):
        if self.settings_clicked:
            self.settingsframe.grid_remove()
            self.settings_clicked = False
        else:
            self.settingsframe.grid()
            self.settings_clicked = True
        
    def change_city(self, location):
        self.location_box.configure(text=location)

    def on_favorite_click(self):
        # Unfavorite Location
        if self.heart_clicked:
            self.heart_clicked = False
        # Favorite Location
        else:
            #Example Implementation:
            #favorite_list.append(current_city)
            self.heart_clicked = True

    def on_left_click(self):
        print("left arrow clicked")
        #Example Implementation (to get the idea):
        #self.favorite_list.shiftLeft()
        #update_city(favorite_list.fetchHead())

    def on_right_click(self):
        print("right arrow clicked")
        #self.favorite_list.shiftLeft()

"""
Sets up the search bar.
"""
class Search:
    def __init__(self, app, weather_app):
        self.app = app
        self.weather_app = weather_app
        self.location = ctk.StringVar()
        self.create_search_entry()

    def create_search_entry(self):
        self.search_entry = ctk.CTkEntry(
            self.app, width=120, height=40, corner_radius=8, border_width=2,
            placeholder_text="Search for a Location", textvariable=self.location
        )
        self.search_entry.grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky="ew")
        """
        search_button = ctk.CTkButton(
            self.app, text="Search", command=self.on_search_submit
        )
        search_button.grid(row=1, column=4, padx=2, pady=1)
        """
        self.search_entry.bind("<Return>", lambda event=None: self.on_search_submit())

    def get_search_text(self):
        print("Location Searched: ", self.location.get())
        return self.location.get()
    
    def on_search_submit(self):
        city = self.get_search_text()
        self.weather_app.update_city(city)
        self.location.set("")
        original = self.search_entry.cget("fg_color")
        self.search_entry.configure(fg_color="light green")
        self.app.after(100, lambda: self.search_entry.configure(fg_color=original))

"""
This is the main box for the current weather to be displayed. There is the temp in F or C and a 
statement about the current conditions.
"""
class WeatherDisplay:
    def __init__(self, app):
        self.app = app
        self.create_display_labels()

    def create_display_labels(self):
        # Temperature Label
        self.temp_label = ctk.CTkLabel(self.app, text="Loading...", font=("Tahoma", 55), fg_color="light grey", height=175, corner_radius=15)
        self.temp_label.grid(row=3, column=2, padx=5, pady=(15,25), sticky="nsew")

        # Weather Condition Label
        self.weather_label = ctk.CTkLabel(self.app, text="Loading...", font=("Tahoma", 40), fg_color="light grey", height=175, corner_radius=15)
        self.weather_label.grid(row=3, column=3, padx=5, pady=(15,25), sticky="nsew")

    def update_weather(self, temperature, condition, unit="F"):
        if unit == "F":
            temperature = temperature * 1.8 + 32
        print(f"Updating weather: {temperature}° {unit}, {condition}")
        self.temp_label.configure(text=f"{temperature}° {unit}")
        self.weather_label.configure(text=condition)

"""
Sets up the buttons above the forecast box to switch between hourly and daily forecast.
"""
class Forecast:
    def __init__(self, app, data_loader, scrollable_area):
        self.app = app
        self.data_loader = data_loader
        self.scrollable_area = scrollable_area
        self.create_forecast_buttons(data_loader.unit)
        self.buttonColors = ["#4da6ff", "#F0F0F0"]


    def create_forecast_buttons(self, unit = "F"):
        self.hourly_button = ctk.CTkButton(
            self.app, text="Hourly", command=lambda: self.select_forecast(1, unit),
            text_color="black", border_width=1, font=("Verdana", 18)
        )
        self.hourly_button.grid(row=5, column=2, padx=0, pady=10)

        self.daily_button = ctk.CTkButton(
            self.app, text="Daily", command=lambda: self.select_forecast(0, unit),
            text_color="black", border_width=0, font=("Verdana", 18)
        )
        self.daily_button.grid(row=5, column=3, padx=0, pady=10)
    
    #hourly = 1; daily = 0
    def select_forecast(self, forecast_type, unit):
        self.hourly_button.configure(fg_color=self.buttonColors[not forecast_type])
        self.hourly_button.configure(border_width= not forecast_type)
        self.daily_button.configure(fg_color=self.buttonColors[forecast_type])
        self.daily_button.configure(border_width=forecast_type)
        self.data_loader.forecast_type = forecast_type
        self.data_loader.update_current()


"""
Main frontend method to receive the API data from the backend and then put it into the correct area.
"""
class DataLoader:
    def __init__(self, weather_display, scrollable_area, city, forecast_type, unit):
        self.city = city
        self.weather_fetcher = initialize(self.city)
        self.weather_display = weather_display
        self.scrollable_area = scrollable_area
        #[daily, hourly]
        self.forecasts = [None, None]
        self.current = None
        self.unit = unit
        self.forecast_type = forecast_type

    def update_city(self, new_city):
        self.city = new_city
        self.weather_fetcher = initialize(self.city)

    def load_data(self):
        self.current = self.weather_fetcher.current
        print("Loading Current")

        self.forecasts[0] = self.weather_fetcher.daily
        self.forecasts[1] = self.weather_fetcher.hourly
        
    def update_current(self):
        if self.current:
            self.weather_display.update_weather(self.current['Temperature'], self.current['Condition'], self.unit) 
            if self.forecasts[0] and self.forecasts[1]:
                self.scrollable_area.update_area(self.forecasts[self.forecast_type], self.forecast_type, self.unit)
            print("Updating current")

"""
Sets up the main box that holds the forecast info. Updates to take the API data and display it.
"""
class ScrollableArea:
    def __init__(self, app):
        self.app = app
        self.create_scrollable_area()

    def create_scrollable_area(self):
        self.forecast_container = ctk.CTkFrame(self.app, corner_radius=10, bg_color="grey")
        self.forecast_container.grid(row=6, column=1, columnspan=4, padx=0, pady=10, sticky="nsew")

        self.forecast_canvas = ctk.CTkCanvas(self.forecast_container)
        self.forecast_canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.forecast_container, command=self.forecast_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.forecast_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.forecast_canvas.bind('<Configure>', self.adjust_frame_width)

        # Create the forecast_frame within the canvas
        self.forecast_frame = ctk.CTkFrame(self.forecast_canvas, bg_color="grey")
        self.canvas_window = self.forecast_canvas.create_window((0, 0), window=self.forecast_frame, anchor="nw")

        # Bind the <Configure> event of the forecast_frame to adjust the scrollregion of the canvas
        self.forecast_frame.bind('<Configure>', lambda e: self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox("all")))


    def adjust_canvas_scrollregion(self, event):
        # Update the scrollregion of the canvas
        self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox("all"))

    def adjust_frame_width(self, event):
        canvas_width = event.width
        self.forecast_canvas.itemconfig(self.canvas_window, width=canvas_width)
        # Update the scrollregion of the canvas
        self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox("all"))

    def update_area(self, forecast, type, unit="F"):
        # Clear existing forecast widgets
        for widget in self.forecast_frame.winfo_children():
            widget.destroy()

        #if type in ["hourly", "daily"]:
        if type in [0, 1]:
            # Iterate over the indices of the forecast lists
            self.forecast_frame.grid_columnconfigure((0, 1, 2, 3), weight=2)
            for i in range(len(forecast['Time'])):
                time = forecast['Time'][i]
                temp = forecast['Temperature'][i]
                if unit == "C":
                    temp = (temp - 32) * 5 / 9 
                condition = forecast['Conditions'][i]
                wind_speed = forecast['Wind Speed'][i]
                wind_dir = forecast['Wind Direction'][i]
                #humidity = forecast['Humidity'][i]
                #dew_point = forecast['Dew Point'][i]

                time_label = ctk.CTkLabel(self.forecast_frame, text=time)
                temp_label = ctk.CTkLabel(self.forecast_frame, text=f"{round(temp, 2)}°{unit}")
                condition_label = ctk.CTkLabel(self.forecast_frame, text=condition)
                wind_label = ctk.CTkLabel(self.forecast_frame, text=f"Wind: {wind_speed} mph {wind_dir}")
                #humidity_label = ctk.CTkLabel(self.forecast_frame, text=f"Humidity: {humidity}%")
                #dew_point_label = ctk.CTkLabel(self.forecast_frame, text=f"Dew Point: {dew_point}° F")

                # Grid these labels
                time_label.grid(row=i, column=0, sticky="ew")
                temp_label.grid(row=i, column=1, sticky="ew")
                condition_label.grid(row=i, column=2, sticky="ew")
                wind_label.grid(row=i, column=3, sticky="ew")
                #humidity_label.grid(row=i, column=4, sticky="ew")
                #dew_point_label.grid(row=i, column=5, sticky="ew")

        # Update the frame and canvas configurations
        self.forecast_frame.update_idletasks()
        self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox("all"))

"""
Class for circularly linked list of favorite city data
"""
class FavoriteList:
    def __init__(self):
        self.head = None

    #Add favorited location
    def append(self, city): 
        if not self.head: #No head node yet, create first entry in list
            self.head = FavoriteNode(city)
            self.head.next = self.head
            self.head.prev = self.head
        else: #Adds new node previous to head node
            newNode = FavoriteNode(city)
            cur = self.head
            while cur.next != self.head:
                cur = cur.next
            cur.next = newNode
            newNode.next = self.head
            newNode.prev = cur
            self.head.prev = newNode

    #For arrow keys, shift right or left in list and [pull data from head node] AFTER CALLING
    def shiftRight(self):
        self.head = self.head.next

    def shiftLeft(self):
        self.head = self.head.prev

    def fetchHead(self):
        return self.head.city

"""
Class for favorite location node in list
"""
class FavoriteNode:
    def __init__(self, city):
        self.city = city
        self.next = None
        self.prev = None


"""
The main class, holds the other classes and holds the actually functionality to launch the window.
"""
class WeatherApp:
    def __init__(self):
        # Initialize the main window
        self.app = ctk.CTk()
        self.setup_window()

        self.configure_layout()
        self.title = ctk.CTkLabel(self.app, text="The Weather App")
        self.title.grid(row=0, column=0, columnspan=6, padx=5, pady=5, sticky="ew")
        
        
        self.search = Search(self.app, self)
        self.weather_display = WeatherDisplay(self.app)
        self.scrollable_area = ScrollableArea(self.app)
        current = current_Location()
        self.current_city = current.location
        self.default_city = "Corvallis"
        self.data_loader = DataLoader(self.weather_display, self.scrollable_area, self.default_city, 1, "F")
        self.forecast = Forecast(self.app, self.data_loader, self.scrollable_area)
        self.navigation = Navigation(self.app, self.data_loader)
    
    def update_city(self, city):
        self.data_loader.update_city(city)
        self.data_loader.load_data()
        self.data_loader.update_current()
        self.navigation.change_city(city)


    def setup_window(self):
        self.app.title("The Weather App")
        self.app.geometry("720x480")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

    def configure_layout(self):
        for i in range(6):
            self.app.grid_columnconfigure(i, weight=1)
        self.app.grid_rowconfigure(6, weight=1)
        

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    weather_app = WeatherApp()
    if weather_app.current_city == None:
        weather_app.update_city(weather_app.default_city)
    else:
        weather_app.update_city(weather_app.current_city)
    weather_app.run()
