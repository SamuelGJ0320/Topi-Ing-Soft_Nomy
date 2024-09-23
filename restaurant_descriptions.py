#importar librerías
import os
from openai import OpenAI
import json
from dotenv import load_dotenv

# Se lee del archivo .env la api key de openai
_ = load_dotenv('api_keys_2.env')
client = OpenAI(
    api_key=os.environ.get('openai_apikey'),
)

# Se carga la lista de restaurantes de restaurants.json
with open('restaurants.json', 'r') as file:
    file_content = file.read()
    restaurants = json.loads(file_content)


#Se genera una función auxiliar que ayudará a la comunicación con la api de openai
#Esta función recibe el prompt y el modelo a utilizar (por defecto gpt-3.5-turbo)
#devuelve la consulta hecha a la api
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content

# Definimos una instrucción general que le vamos a dar al modelo 
instruction = "Vas a actuar como un crítico gastronómico que sabe describir de forma clara, concisa y precisa \
cualquier restaurante en menos de 200 palabras."

# Podemos iterar sobre todos los restaurantes para generar la descripción.
for i in range(len(restaurants)):
    restaurant_name = restaurants[i]['nombre']
    prompt = f"{instruction} Haz una descripción del restaurante {restaurant_name}."
    
    # Utilizamos la función para comunicarnos con la API
    response = get_completion(prompt)
    restaurants[i]['description'] = response 

    print(f"Descripción de {restaurant_name}: {response}")
    print(f"restaurante {i + 1} de {len(restaurants)}")

file_path = "restaurant_descriptions.json"

# Write the data to the JSON file
with open(file_path, 'w') as json_file:
    json.dump(restaurants, json_file, indent=4)

print(f"Data saved to {file_path}")
