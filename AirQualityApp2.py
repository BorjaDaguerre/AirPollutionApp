import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.garden.graph import Graph, MeshLinePlot

from datetime import date
import pandas as pd
class AirQualityApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.layout.add_widget(Image(source='air-pollution.png'))

        self.city_name = TextInput(multiline=False, hint_text="Enter city name")
        self.layout.add_widget(self.city_name)


        self.button = Button(text='Get Air Quality', on_press=self.air_quality)
        self.layout.add_widget(self.button)


        self.graph = Graph(xlabel='Hours', ylabel='AQI (PM10)')
        self.plot = MeshLinePlot(color=[0, 1, 0, 1])
        self.plot.line_width = 2
        self.graph.add_plot(self.plot)
        self.layout.add_widget(self.graph)

        self.graph.xlabel = 'Time'
        self.graph.ylabel = 'AQI (PM10)'

        self.info = Label(text='')
        self.layout.add_widget(self.info)

        quit_button = Button(text='Quit', size_hint=(None, None))
        quit_button.size = (100, 50)
        quit_button.bind(on_press=self.quit_app)
        self.layout.add_widget(quit_button)

        return self.layout

    def air_quality(self, instance):
        today = date.today().strftime("%Y-%m-%d")
        city_name_text = self.city_name.text

        query = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={city_name_text}").json()
        lat = query[0].get('lat')
        lon = query[0].get('lon')
        response = requests.get(f'https://air-quality-api.open-meteo.com/v1/air-quality?latitude='
                                f'{lat}&longitude={lon}&hourly=pm10,pm2_5&start_date={today}&end_date={today}').json()


        aqi_pm10 = response.get('hourly').get('pm10')
        dates = pd.to_datetime(response.get('hourly').get('time'), format='%Y-%m-%dT%H:%M')
        hours = dates.strftime('%H')

        # self.info.text = str(self.aqi_pm10)

        self.plot.points = [(int(hour), int(aqi)) for hour, aqi in zip(hours, aqi_pm10)]
        self.info.text = f'AQI PM10: {aqi_pm10[-1]}'  # Display the latest AQI value

    def quit_app(self, instance):
        App.get_running_app().stop()


if __name__ == "__main__":
    AirQualityApp().run()
