#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import storage
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from requests import get
import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from models.user import User
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
import os
from flask_bcrypt import Bcrypt, check_password_hash
from models.property import Properties

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = os.urandom(16)
login_manager = LoginManager(app)
login_manager.login_view = 'login'



class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(min=4, max=25), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    mode = SelectField('Mode', choices=[('tenant', 'Tenant'), ('landlord', 'Landlord')], validators=[DataRequired()])
    submit = SubmitField('login')

class RegistrationForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(min=4, max=25), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match'), Length(min=8)])
    submit = SubmitField('signup')

    def validate_email(self, email):
        #fetch email from form
        email = email.data
        users = storage.all(User)
        for user in users.values():
            if user.email == email:
                raise ValidationError('use a different email')

class PropertyForm(FlaskForm):
    property_name = StringField('Property name', validators=[DataRequired()])
    adress = StringField('Adress')
    make = StringField('type of house')
    submit = SubmitField('Add Property')


@app.teardown_appcontext
def close(error):
    storage.close

@login_manager.user_loader
def load_user(user_id):
    return storage.get(User, user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        mode = form.mode.data
        email= form.email.data
        users = storage.all(User)
        user = next((user for user in users.values() if user.email == email), None)
        if user and check_password_hash(user.password, form.password.data):
            if mode == 'tenant':
                login_user(user)
                flash('Logged in successfully.')
                return redirect(url_for('tenant'))
            else:
                login_user(user)
                flash('Logged in successfully.')
                return redirect(url_for('landlord'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)

#@app.route('/landlord', methods=['GET', 'POST'])
#@login_required
#def landlord():
#    form = PropertyForm()

#    if form.validate_on_submit():
        # Create a new property
#        property_name = form.property_name.data
#        address = form.address.data
        # You might want to link the new property to the logged-in landlord user here
#        new_property = Property(name=property_name, address=address)
#        storage.new(new_property)
#        storage.save()
#        flash('Property added successfully.')
#        return redirect(url_for('landlord'))

    # Retrieve properties from the database
#    properties = storage.all(Property)
#    print("Properties:", properties)

#    return render_template('landlord.html', form=form, properties=properties)

#@app.route('/landlord/edit/<property_id>', methods=['GET', 'POST'])
#@login_required
#def edit_property(property_id):
#    form = PropertyForm()
#    property_to_edit = storage.get(Property, property_id)
#
#    if property_to_edit is None:
#        flash('Property not found.')
#        return redirect(url_for('landlord'))

#    if form.validate_on_submit():
#        property_to_edit.name = form.property_name.data
#        property_to_edit.address = form.address.data
#        storage.save()
#        flash('Property updated successfully.')
#        return redirect(url_for('landlord'))

#    form.property_name.data = property_to_edit.name
#    form.address.data = property_to_edit.address

#    return render_template('edit_property.html',)

#@app.route('/landlord/delete/<property_id>', methods=['POST'])
#@login_required
#def delete_property(property_id):
#    property_to_delete = storage.get(Property, property_id)
#
 #   if property_to_delete:
#        storage.delete(property_to_delete)
#        storage.save()
#        flash('Property deleted successfully.')
 #   else:
  #      flash('Property not found.')

   # return redirect(url_for('landlord'))



@app.route('/tenant')
@login_required
def tenant():
    # Make API call to get tenant property data
   # api_tenant = 'https://your_tenant_api_url'
    #response_tenant = get(api_tenant)
   # data_tenant = json.loads(response_tenant.text)
    return render_template('tenant.html')

@app.route('/landlord',  methods=['GET', 'POST'])
@login_required
def landlord():
    # Make API call to get landlord property data
    #api_landlord = 'https://your_landlord_api_url'
    #response_landlord = get(api_landlord)
    #data_landlord = json.loads(response_landlord.text)
    if current_user.is_authenticated:
        user_id = current_user.id
        form = PropertyForm()
        if form.validate_on_submit():
           new_property = Properties(user_id=user_id, property_name=form.property_name.data, adress=form.adress.data, make=form.make.data)
           storage.new(new_property)
           storage.save()
        properties = storage.all(Properties)
        return render_template('landlord.html', properties=properties, form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(email=form.email.data, password=hashed_password)
        storage.new(new_user)
        storage.save()
        flash('New user has been created.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug='True')
