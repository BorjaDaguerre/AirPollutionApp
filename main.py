from datetime import date
import requests
import pandas as pd

from kivy.app import App
from kivy.uix.image import Image
from kivy.garden.graph import MeshLinePlot, Graph

from datetime import date
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.graph import Graph, MeshLinePlot

class MainApp(App):

    def build(self):
        return MyRootWidget()

    def fetch_air_quality(self, city_name):
        results = self.get_air_quality(city_name)
        self.root.ids.message_label.text = results

    def get_air_quality(self, city_name):
        today = date.today().strftime("%Y-%m-%d")
        query = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={city_name}").json()
        lat = query[0].get('lat')
        lon = query[0].get('lon')
        response = requests.get(f'https://air-quality-api.open-meteo.com/v1/air-quality?latitude='
                               f'{lat}&longitude={lon}&hourly=pm10,pm2_5&start_date={today}&end_date={today}').json()

        dates = pd.to_datetime(response.get('hourly').get('time'), format='%Y-%m-%dT%H:%M')
        self.hours = dates.strftime('%H')
        self.aqi_pm10 = response.get('hourly').get('pm10')
        self.display_air_quality(self.aqi_pm10)  # Pass the air quality data for the graph
        return f'The air quality in {city_name} on the {date.today().strftime("%d")} is ' + str(self.aqi_pm10[0]) + ' pm10'

    def display_air_quality(self, aqi_data):
        # Access the Graph widget
        graph = self.root.ids.graph

        # Create a new plot with the fetched air quality data
        plot = MeshLinePlot(color=[1, 1, 0, 1])
        plot.points = [(i, aqi) for i, aqi in enumerate(aqi_data)]
            
        # Add the new plot to the graph
        graph.add_plot(plot)

class MyRootWidget(BoxLayout):
    pass

if __name__ == "__main__":
    MainApp().run()



