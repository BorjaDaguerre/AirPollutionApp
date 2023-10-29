import requests
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt

today = date.today().strftime("%Y-%m-%d")
city_name = input()

query= requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={city_name}").json()
lat = query[0].get('lat')
lon = query[0].get('lon')
response = requests.get(f'https://air-quality-api.open-meteo.com/v1/air-quality?latitude='
                        f'{lat}&longitude={lon}&hourly=pm10,pm2_5&start_date={today}&end_date={today}').json()

aqi_pm10 = response.get('hourly').get('pm10')
dates = pd.to_datetime(response.get('hourly').get('time'), format='%Y-%m-%dT%H:%M')
hours = dates.strftime('%H')
data = pd.DataFrame(index = hours, data = aqi_pm10, columns = ['aqi pm10'])

aqi_colors = {
    (0, 10): ['green', 'Good'],          # Good
    (10, 20): ['limegreen', 'Fair'],     # Fair
    (20, 25): ['yellow', 'Moderate'],        # Moderate
    (25, 50): ['orange', 'Poor'],        # Poor
    (50, 75): ['red', 'Very poor'],           # Very poor
    (75, 800): ['darkred', 'Extremly poor']       # Extremely poor
}


# Create a color list based on AQI values
colors = [next(color[0] for (min_aqi, max_aqi), color in aqi_colors.items()
          if min_aqi <= aqi <= max_aqi) for aqi in aqi_pm10]

# Create a DataFrame
data = pd.DataFrame(index=hours, data=aqi_pm10, columns=['aqi pm10'])

# Create a figure and axis
fig, ax = plt.subplots()

# Scatter plot with color-coded dots
ax.scatter(x=hours, y=data['aqi pm10'], c=colors, s=100, edgecolor='black', linewidths=1, alpha=0.7)

# Customize labels and title
ax.set_xlabel('Hours')
ax.set_ylabel('AQI (PM10)')
ax.set_title('Air Quality Index (PM10) Over Time')

colors = [color[0] for color in aqi_colors.values()  ]
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=label[0],
                      markersize=10, label=label[1]) for (min_aqi, max_aqi), label in aqi_colors.items()]


ax.legend(handles=handles, title='AQI Levels')

# Show the plot
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()