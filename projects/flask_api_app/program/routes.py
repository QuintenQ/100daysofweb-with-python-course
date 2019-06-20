from datetime import datetime

import requests
from flask import render_template, request
from requests.exceptions import HTTPError

from program import app

@app.route('/')
@app.route('/index')
def index():
    timenow = str(datetime.today())
    return render_template('index.html', time = timenow)

@app.route('/chuck')
def chuck():
    joke = get_chuck_joke()
    return render_template('chuck.html',
                            joke = joke)


@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    pokemon = []
    if request.method == 'POST' and 'pokecolour' in request.form:
        colour = request.form.get('pokecolour')
        if colour == '':
            return render_template('pokemon.html', pokemon = False)
        pokemon = get_poke_colour(colour)
    if pokemon == False:
        return render_template('pokemon.html', pokemon = False)
    else:
        return render_template('pokemon.html', pokemon = pokemon)
    return render_template('pokemon.html', pokemon = pokemon)

def get_chuck_joke():
    r = requests.get('https://api.chucknorris.io/jokes/random')
    data = r.json()
    return data['value']

def get_poke_colour(colour):
    try:
        r = requests.get('https://pokeapi.co/api/v2/pokemon-color/' + colour.lower())
        r.raise_for_status()
    except HTTPError as http_err:
        return False
    except Exception as err:
        return False
    else:
       
        pokedata = r.json()
        pokemon = []

        for i in pokedata['pokemon_species']:
            pokemon.append(i['name'])

        return pokemon

"""
Todo

2. Add in some error handling on the user input. Eg: Right now, entering a number or an invalid colour (not in the API) will break the app - account for these scenarios.
3. Check out the rest of the Pokemon API endpoints and test printing other types of Pokemon data.
4. If you're feeling really brave: on our existing app (printing the names of a Pokemon of a specific colour), have the app return more than just the Pokemon name. Eg: the "Nature", the "Form", the "Habitat"..
"""
