from django.shortcuts import render
from django.http import HttpResponse

from django.template import loader
import requests
import random

# Create your views here.

def get_pokemon_info(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        pokemon_data = response.json()
        pokemon_info = {
            "id": pokemon_data["id"],
            "name": pokemon_data["name"],
            "height": pokemon_data["height"]/10,
            "weight": pokemon_data["weight"]/10,
            "abilities": [ability["ability"]["name"] for ability in pokemon_data["abilities"]],
            "types": [type_data["type"]["name"] for type_data in pokemon_data["types"]]
        }
        return pokemon_info
    else:
        return None

def get_pokemon_description(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}/"
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()
        pokemon_info = {
            "description": pokemon_data["flavor_text_entries"][0]["flavor_text"]
        }
        return pokemon_info
    else:
        return None

def index(request):

    pokemon_name = ("pikachu")

    if request.method == 'POST':
        if request.POST.get('textfield', None) == "gen1":
            pokemon_name = str(random.randint(1,151))
        elif request.POST.get('textfield', None) == "gen2":
            pokemon_name = str(random.randint(152,251))
        elif request.POST.get('textfield', None) == "gen3":
            pokemon_name = str(random.randint(252,386))
        elif request.POST.get('textfield', None) == "random":
            pokemon_name = str(random.randint(1,251))
        else:
            pokemon_name = request.POST.get('textfield', None)

    pokemon_info = get_pokemon_info(pokemon_name)
    pokemon_des = get_pokemon_description(pokemon_name)
    
    # template = loader.get_template('dex.html')
    # return HttpResponse(template.render())
    # return HttpResponse("This is the 1st version of my pokedex.")
    # return render(request, 'dex.html', {'text':'Hello'})
    
    return render(request, 'dex.html', 
                {'Id': pokemon_info['id'],
                 'Name': pokemon_info['name'].upper(), 
                 'Description': pokemon_des['description'],
                 'Height': pokemon_info['height'], 
                 'Weight': pokemon_info['weight'], 
                 'Abilities': pokemon_info['abilities'], 
                 'Types': pokemon_info['types']})