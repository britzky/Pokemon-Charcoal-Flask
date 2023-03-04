from flask import render_template, request, url_for, flash, redirect 
import requests
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user
from app.forms import PokemonForm, SignUpForm, LoginForm
from app.models import User
from app import app

# Routes section
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/logout', methods=['GET'])
def logout():
    if current_user:
        logout_user()
        flash('You have logged out!', 'warning')
        return redirect(url_for('login'))

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit:
        # Grabbing our form data and storing into a dict
        new_user_data = {
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email': form.email.data.lower(),
            'password': form.password.data
        }
        # Create instance of user
        new_user = User()

        # Implementing values from our form data for our instance
        new_user.from_dict(new_user_data)

        # Save to our database
        new_user.save_to_db()
        flash('You have successfully signed up!', 'success')
        return redirect(url_for('login'))
    return render_template('sign_up.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit:
        email = form.email.data.lower()
        password = form.password.data

        # query from our database
        queried_user = User.query.filter_by(email=email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Sucessfully logged in! Welcome back, {queried_user.first_name}!', 'success' )
            return redirect(url_for('home'))
        else:
            error = 'Invalid email or password'
            flash(f'{error}', 'danger')
    return render_template('login.html', form=form)

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    form = PokemonForm()
    if request.method == 'POST' and form.validate_on_submit:
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
                'type': pokemon_data['types'][0]['type']['name'],
                'small_sprite': pokemon_data['sprites']['front_default']
            }
            new_pokemon_data.append(info)
            return render_template('pokemon.html', new_pokemon_data=new_pokemon_data, form=form)
        else:
            error = 'That\'s not a pokemon!'
            return render_template('pokemon.html', error=error, form=form)
    return render_template('pokemon.html', form=form)