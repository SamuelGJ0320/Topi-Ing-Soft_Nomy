import pandas as pd
import json

# Lee el archivo CSV
df = pd.read_csv('restaurants_initial.csv')

# Guarda el dataframe como un archivo JSON
df.to_json('restaurants.json', orient='records')

with open ('restaurants.json') as file:
    restaurants = json.load(file)

for i in range(50):   # 50 son los restaurantes que tenemos en la base de datos y por ende los que se van a cargar
    restaurant = restaurants[i]
    print(restaurant)
    break

