from flask import render_template, request, flash, url_for, redirect
import requests
from flask_login import login_required, current_user
from app.blueprints.auth.forms import PokemonForm
from app.blueprints.main import main
from app.models import Pokemon, User, team

# Routes section
@main.route('/', methods=['GET'])
@login_required
def home():
    return render_template('home.html')

@main.route('/pokemon', methods=['GET','POST'])
@login_required
def pokemon():
    form = PokemonForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data.lower()
        url = f'https://pokeapi.co/api/v2/pokemon/{name}' 
        response = requests.get(url)
        if response.ok:
            pokemon_data = response.json()
            new_pokemon_data = []
            if pokemon_data['sprites']['other']['dream_world']['front_default'] is not None:
                sprite_url = pokemon_data['sprites']['other']['dream_world']['front_default']
            else:
                sprite_url = pokemon_data['sprites']['front_default']

            info = {
                'name': pokemon_data['forms'][0]['name'],
                'ability': pokemon_data["abilities"][0]["ability"]["name"],
                'base_experience': pokemon_data['base_experience'],
                'sprite': sprite_url,        
                'attack_base_stat': pokemon_data['stats'][1]['base_stat'],
                'hp_base_stat': pokemon_data['stats'][0]['base_stat'],
                'defense_base_stat': pokemon_data['stats'][2]['base_stat'],
                'pokemon_type': pokemon_data['types'][0]['type']['name'],
                'small_sprite': pokemon_data['sprites']['front_default']
            }
            new_pokemon_data.append(info)
            return render_template('pokemon.html', new_pokemon_data=new_pokemon_data, form=form)
        else:
            error = 'That\'s not a pokemon!'
            return render_template('pokemon.html', error=error, form=form)
    return render_template('pokemon.html', form=form)

@main.route('/run_away', methods=['GET', 'POST'])
@login_required
def run_away():
    if request.method:
        return redirect(url_for('main.pokemon'))


@main.route('/catch/<pokemon>')
@login_required
def catch(pokemon):
    name = Pokemon.query.filter_by(name=pokemon).first()
    if current_user.check_team(name):
        flash(f'You already have {pokemon.title()}', 'danger')
        return redirect(url_for('main.pokemon'))
    else:
        if name:
            current_user.catch(name)
            flash(f'you caught {pokemon.title()}')
            return redirect(url_for('main.pokemon'))
        else:
            name = pokemon
            url = f'https://pokeapi.co/api/v2/pokemon/{name}' 
            response = requests.get(url)
            if response.ok:
                pokemon_data = response.json()
            # Grabbing our  and storing into a dict
                pokemon_data = {
                    'name': pokemon_data['forms'][0]['name'],
                    'ability': pokemon_data["abilities"][0]["ability"]["name"],
                    'base_experience': pokemon_data['base_experience'],       
                    'attack_base_stat': pokemon_data['stats'][1]['base_stat'],
                    'hp_base_stat': pokemon_data['stats'][0]['base_stat'],
                    'defense_base_stat': pokemon_data['stats'][2]['base_stat'],
                    'pokemon_type': pokemon_data['types'][0]['type']['name'],
                    'small_sprite': pokemon_data['sprites']['front_default']
                }
                # Create instance of pokemon
                new_pokemon = Pokemon()
            if current_user.max_pokemon():
                flash(f'Your team is already full!', 'danger')
                return redirect(url_for('main.pokemon'))
            else:
                
                # Implementing values from our form data for our instance
                new_pokemon.from_dict(pokemon_data)
                # Save to our database
                new_pokemon.save_to_db()
                # Catch the pokemon with the current user
                current_user.catch(new_pokemon)
                flash(f'You caught {pokemon.title()}', 'success')
                return redirect(url_for('main.pokemon'))
             

@main.route('/release/<name>')
@login_required
def release(name):
    team = current_user.pokemon
    for pokemon in team:
        if pokemon.name == name:
            current_user.release(pokemon)
            flash(f'Successfully removed {pokemon.name.title()}!', 'success')
    return redirect(url_for('main.pokemon'))

@main.route('/challenge/<int:user_id>', methods=['GET', 'POST'])
@login_required
def challenge(user_id):
    trainer_id = User.query.get(user_id)
    user = current_user
    trainer_pokemon = trainer_id.pokemon
    user_pokemon = current_user.pokemon

    user_attack_sum = sum(pokemon.attack_base_stat for pokemon in user_pokemon)
    trainer_attack_sum = sum(pokemon.hp_base_stat for pokemon in trainer_pokemon)
    user_hp_sum = sum(pokemon.hp_base_stat for pokemon in user_pokemon)
    trainer_hp_sum = sum(pokemon.hp_base_stat for pokemon in trainer_pokemon)

    user_wins = user_attack_sum > trainer_hp_sum
    user_loses = trainer_attack_sum > user_hp_sum
    user_ties = user_attack_sum == trainer_hp_sum

    return render_template('challenge.html',user_ties=user_ties, user_loses=user_loses, trainer_attack_sum=trainer_attack_sum, user_hp_sum=user_hp_sum, trainer_pokemon=trainer_pokemon, user_pokemon=user_pokemon, trainer_id=trainer_id, user=user, user_attack_sum=user_attack_sum, trainer_hp_sum=trainer_hp_sum, user_wins=user_wins)

  
    # return render_template('challenge.html', trainer_pokemon=trainer_pokemon, user_pokemon=user_pokemon, trainer_id=trainer_id, user=user)
      


#view user pokemon
@main.route('/my_pokemon', methods=['GET'])
@login_required
def my_pokemon():
    user_pokemon = current_user.pokemon
    return render_template('my_pokemon.html', user_pokemon=user_pokemon)

#All users pokemon
@main.route('/trainers',methods=['GET'])
@login_required
def trainers():
    users = User.query.all()
    trainers = []
    for user in users:
        if user != current_user:
            trainers.append({
                'first_name': user.first_name,
                'last_name': user.last_name,
                'pokemon': user.pokemon,
                'id': user.id
            })
    return render_template('trainers.html', trainers=trainers)





    

