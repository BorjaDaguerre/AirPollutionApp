
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.graph import Graph, MeshLinePlot



import requests
import pandas as pd
from datetime import date



class AirQualityApp(App):
    def build(self):

        self.window = BoxLayout(orientation='vertical')
        self.window.add_widget(Image(source='air-pollution.png'))

        self.city_name = TextInput(multiline = False)
        self.window.add_widget(self.city_name)

        self.button = Button(text='Air Quality')
        self.button.bind(on_press=self.air_quality)
        self.window.add_widget(self.button)

        self.info = Label(text=' ')
        self.window.add_widget(self.info)

        self.plot_layout = BoxLayout(orientation = 'vertical')
        self.window.add_widget(self.plot_layout)

        return self.window
    def air_quality(self, instance):
        today = date.today().strftime("%Y-%m-%d")
        city_name_text = self.city_name.text

        query = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={city_name_text}").json()
        lat = query[0].get('lat')
        lon = query[0].get('lon')
        response = requests.get(f'https://air-quality-api.open-meteo.com/v1/air-quality?latitude='
                                f'{lat}&longitude={lon}&hourly=pm10,pm2_5&start_date={today}&end_date={today}').json()

        self.aqi_pm10 = response.get('hourly').get('pm10')
        dates = pd.to_datetime(response.get('hourly').get('time'), format='%Y-%m-%dT%H:%M')
        self.hours = dates.strftime('%H')

        #self.info.text = str(self.aqi_pm10)

        self.display_graph(aqi_pm10)
    def display_graph(self, aqi_pm10):
        fig, ax = plt.subplots()

        # Create a line plot
        ax.plot(x, y, marker='o', linestyle='-')

        # Save the Matplotlib figure as an image
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        pil_image = PILImage.open(buf)

        # Convert the PIL image to Kivy Image
        kivy_image = Image(texture=pil_image.texture)

        # Add the Kivy Image to the layout
        layout.add_widget(kivy_image)


if __name__ == "__main__":
    AirQualityApp().run()
