from flask import Flask, render_template, request
import requests 

app = Flask(__name__)

@app.route('/ergast', methods=['GET', 'POST'])
def ergast():
    print(request.method)
    if request.method == 'POST':
        name = request.form.get('pokemon').lower()
        url = f'https://pokeapi.co/api/v2/pokemon/{name}' 
        response = requests.get(url)
        if response.ok:
            pokemon_data = response.json()
            new_pokemon_data = []
            info = {
                'name': pokemon_data['forms'][0]['name'],
                'ability': pokemon_data["abilities"][0]["ability"]["name"],
                'base_experience': pokemon_data['base_experience'],
                'sprite': pokemon_data['sprites']['other']['dream_world']['front_default'],        
                'attack_base_stat': pokemon_data['stats'][1]['base_stat'],
                'hp_base_stat': pokemon_data['stats'][0]['base_stat'],
                'defense_base_stat': pokemon_data['stats'][2]['base_stat']
            }
            new_pokemon_data.append(info)
            return render_template('ergast.html', new_pokemon_data=new_pokemon_data)
        else:
            error = 'That\'s not a pokemon!'
            return render_template('ergast.html', error=error)
    return render_template('ergast.html')