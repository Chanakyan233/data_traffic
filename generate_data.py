import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def create_dummy_data(filename="traffic_accidents.csv", num_records=1000):
    # Setup choices for dummy data
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
    weather_conds = ['Clear', 'Rain', 'Fog', 'Snow', 'Cloudy']
    road_conds = ['Dry', 'Wet', 'Ice', 'Snow', 'Gravel']
    severities = ['Low', 'Moderate', 'Severe', 'Fatal']

    # Base coords roughly around these cities
    city_coords = {
        'New York': (40.7128, -74.0060),
        'Los Angeles': (34.0522, -118.2437),
        'Chicago': (41.8781, -87.6298),
        'Houston': (29.7604, -95.3698),
        'Phoenix': (33.4484, -112.0740)
    }

    start_date = datetime(2023, 1, 1)
    
    data = []
    
    for _ in range(num_records):
        city = random.choice(cities)
        base_lat, base_lon = city_coords[city]
        
        # Add a random offset for coordinates to spread accidents around the city
        lat = base_lat + random.uniform(-0.1, 0.1)
        lon = base_lon + random.uniform(-0.1, 0.1)
        
        # Random date and time within the past year
        random_days = random.randint(0, 365)
        accident_date = start_date + timedelta(days=random_days)
        time_str = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
        
        weather = random.choice(weather_conds)
        road = random.choice(road_conds)
        
        # Adjust severity probability based on weather/road conditions
        if weather in ['Rain', 'Snow', 'Fog'] or road in ['Wet', 'Ice']:
            severity = random.choices(severities, weights=[10, 30, 40, 20])[0]
        else:
            severity = random.choices(severities, weights=[50, 30, 15, 5])[0]
            
        # Introduce some missing values randomly for data cleaning practice
        if random.random() < 0.05:
            weather = np.nan
        if random.random() < 0.05:
            road = np.nan
            
        data.append({
            'Date': accident_date.strftime('%Y-%m-%d'),
            'Time': time_str,
            'City': city,
            'Latitude': lat,
            'Longitude': lon,
            'Weather_Condition': weather,
            'Road_Condition': road,
            'Severity': severity
        })

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"✅ Generated {num_records} dummy accident records into '{filename}'.")

if __name__ == "__main__":
    create_dummy_data()