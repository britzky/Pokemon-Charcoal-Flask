from app import db, login
from flask_login import UserMixin # Only use on your User Class
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

team = db.Table('team',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    pokemon = db.relationship(
        'Pokemon', secondary=team, backref='trainers', lazy='dynamic'
    )
    
    
    # hashes our password
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # check password hash
    def check_hash_password(self, login_password):
        return check_password_hash(self.password, login_password)
    
    # Use this method to register our user attributes
    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    def update_profile(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
    
    # Save to our database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    # release pokemon
    def release(self, pokemon):
        db.session.delete(pokemon)
        db.session.commit()
    
    # Update database
    def update_to_db(self):
        db.session.commit()
    
    #add pokemon to team
    def catch(self, pokemon):
        self.pokemon.append(pokemon)
        db.session.commit()

    #check team
    def check_team(self, pokemon):
        if pokemon in self.pokemon:
            return True
        else:
            return False
     #how many pokemon each user can have   
    def max_pokemon(self):
        if len(self.pokemon.all()) >= 6:
            return True
        else: 
            return False
    

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ability = db.Column(db.String)
    base_experience = db.Column(db.Integer)
    attack_base_stat = db.Column(db.Integer)
    hp_base_stat = db.Column(db.Integer)
    defense_base_stat = db.Column(db.Integer)
    pokemon_type = db.Column(db.String) 
    small_sprite = db.Column(db.String)
    
    def from_dict(self, data):
        self.name = data['name']
        self.ability = data['ability']
        self.base_experience = data['base_experience']
        self.attack_base_stat = data['attack_base_stat']
        self.hp_base_stat = data['hp_base_stat']
        self.defense_base_stat = data['defense_base_stat']
        self.pokemon_type = data['pokemon_type']
        self.small_sprite = data['small_sprite']
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
