from flask import render_template, request, url_for, flash, redirect
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from app.blueprints.auth.forms import SignUpForm, LoginForm, EditProfileForm
from app.models import User
from app.blueprints.auth import auth

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out!', 'warning')
        return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
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
        return redirect(url_for('auth.login'))
    return render_template('sign_up.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('main.home'))
        else:
            error = 'Invalid email or password'
            flash(f'{error}', 'danger')
    return render_template('login.html', form=form)

@auth.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit:
        # Grabbing our form data and storing into a dict
        new_user_data = {
            'first_name': form.first_name.data.title(),
            'last_name': form.last_name.data.title(),
            'email': form.email.data.lower(),
            'password': current_user.password,
            'profile_image': form.profile_image.data 
        }
        #cheeck if the email has changed
        if new_user_data['email'] != current_user.email:
            # query from our db based on email to change
            queried_user = User.query.filter_by(email=new_user_data['email']).first()
            if queried_user:
                flash('Email already exists', 'danger')
                return redirect(url_for('auth.edit_profile'))
            
        #add changes to database
        current_user.update(new_user_data)
        current_user.save_to_db()
        flash('Profile updated', 'success')
        return redirect(url_for('main.home'))
    return render_template('edit_profile.html', form=form)
