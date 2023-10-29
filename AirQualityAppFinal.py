import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.garden.graph import Graph, LinePlot

from datetime import date
import pandas as pd


class AirApp(App):
    def build(self):
        return Plotter()
class Plotter(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.graph = Graph(tick_color=[0, 1, 1, 1],
                           border_color=[1, 1, 1, 0.5],
                           x_grid=True, y_grid=True,
                           x_grid_label=True,
                           y_grid_label=False)

        self.data = self.air_quality
        self.plot_x = self.data.hours
        self.plot_y = self.aqi_pm10
        self.plot = LinePlot(color=[1, 1, 0, 1], line_width=1.5)

        
        
    def air_quality(self, instance):
        today = date.today().strftime("%Y-%m-%d")
        city_name_text = self.city_name.text

        query = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={city_name_text}").json()
        lat = query[0].get('lat')
        lon = query[0].get('lon')
        response = requests.get(f'https://air-quality-api.open-meteo.com/v1/air-quality?latitude='
                                f'{lat}&longitude={lon}&hourly=pm10,pm2_5&start_date={today}&end_date={today}').json()


        self.aqi_pm10 = int(response.get('hourly').get('pm10'))
        dates = pd.to_datetime(response.get('hourly').get('time'), format='%Y-%m-%dT%H:%M')
        self.hours = int(dates.strftime('%H'))



AirApp().run()