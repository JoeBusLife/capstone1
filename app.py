import os
from types import MethodType

from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
# from psycopg2.errors import UniqueViolation
from flask_login import LoginManager, login_manager, login_user, login_required, logout_user, current_user

from forms import UserSignupForm, UserLoginForm, UserEditForm, PropertySearchForm, PropertyForm, PropertyEditForm, PropertyCompareForm, form_creator
from models import db, connect_db, User, Property, SavedProperty
from werkzeug.datastructures import MultiDict

import requests
from helpers import *
from locale import currency
import json


app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///property_cat'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "qwertyzog")
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_disabled = False
app.config['USE_SESSION_FOR_NEXT'] = True

# External APIs for property info
estated_api_sandbox = "https://sandbox.estated.com/v4/property"
estated_api = "https://apis.estated.com/v4/property"
estated_api_token_sandbox = os.environ.get('estated_api_token_sandbox')
estated_api_token = os.environ.get('estated_api_token')
token = estated_api_token_sandbox
estated_api_baseURL = estated_api_sandbox

# External API for rent estimate
rm_rent_estimate_api = "https://realtymole-rental-estimate-v1.p.rapidapi.com/rentalPrice"
rm_rent_estimate_headers = {
    'x-rapidapi-host': "realtymole-rental-estimate-v1.p.rapidapi.com",
    'x-rapidapi-key': os.environ.get('rm_rent_estimate_key')
    }



@app.before_request
def before_request():
    """  """
    # print("===========================================")
    # print(request.path)

    skip_pages = ['/login', '/signup', 'static']
    
    if not any(path in request.path for path in skip_pages):
        if session.get('prop_to_save'):
            session.pop('prop_to_save')
            print("===============to_save================")

        if session.get('next'):
            session.pop('next')
            print("================next=================")


@login_manager.user_loader
def load_user(username):
    
    return User.query.get(username)

    
@app.route('/')
def homepage():
    """Show homepage"""
    form = form_creator(PropertySearchForm(), required=False)
    
    return render_template('index.html', form=form)  


def save_prop_after_login(prop_to_save):
    prop_id = prop_to_save.pop('prop_id', None)
    save_name = prop_to_save.pop('save_name', None)
    # save_changes = prop_to_save.pop('save_changes', None)
    
    prop = Property.query.get(prop_id)
    prop.saved_state()
    
    if prop.no_saves:
        prop.save_changes(prop_to_save)
    else:
        new_prop = Property.save_new(prop_to_save)
        prop_id = new_prop.id
    
    new_SP = SavedProperty(save_name=save_name, username=current_user.username, property_id=prop_id)
    db.session.add(new_SP)
    db.session.commit()
    
    session.pop(f'prop_changes_id{prop.id}', None)
    
    flash(f'Property "{new_SP.save_name}" has been saved', "success")
    
    return prop_id


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    
    if current_user.is_authenticated:
        return redirect("/")
    
    form = form_creator(UserSignupForm())
    if request.method == 'GET':
        bad_form_data_signup = session.pop('bad_form_data', None)
        if bad_form_data_signup:
            form = form_creator(UserSignupForm(MultiDict(bad_form_data_signup)))
            form.validate()
        
        return render_template('signup.html', form=form)

    if form.validate_on_submit():
        try:
            form_data = {k: v for k, v in form.data.items() if k != "csrf_token"}
            new_user = User.signup(**form_data)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)

        except IntegrityError as e:
            flash("Internal Server Error", 'danger')
            
            return render_template('signup.html', form=form)

        prop_to_save = session.get('prop_to_save')
        if prop_to_save:
            prop_id = save_prop_after_login(prop_to_save)
            
            return redirect(url_for('property_show',prop_id=prop_id))
        
        return redirect(session.get('next') or '/')

    session['bad_form_data_signup'] = request.form
    return redirect(url_for('signup'))


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    if current_user.is_authenticated:
        return redirect("/")
    
    form = form_creator(UserLoginForm())
    if request.method == 'GET':
        bad_form_data_login = session.pop('bad_form_data', None)
        if bad_form_data_login:
            form = form_creator(UserLoginForm(MultiDict(bad_form_data_login)))
            form.validate()
        
        return render_template('login.html', form=form)
    
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            login_user(user)
            prop_to_save = session.get('prop_to_save')
            if prop_to_save:
                prop_id = save_prop_after_login(prop_to_save)

                return redirect(url_for('property_show', prop_id=prop_id))
            
            flash(f"Hello, {user.username}!", "success")
            return redirect(session.get('next') or '/')
        
        else:
            flash("Invalid credentials.", 'danger')
    
    session['bad_form_data_login'] = request.form
    return redirect(url_for('login'))

    
@app.route('/logout')
def logout():
    """Handle logout of user."""

    if not current_user.is_authenticated:
        return redirect("/")

    logout_user()
    flash("Succesfully logged out", "success")
    
    return redirect('/login')


@app.route('/property/search', methods=['POST'])
def property_search():
    """  """
    
    form = form_creator(PropertySearchForm(), required=False)
    if form.validate_on_submit():
        address = form.address.data
        print('================= +++ =================')
        print(address)
        data = requests.get(estated_api_baseURL, params={"token": token, "combined_address": address}).json()
        
        print(data)
        if not data.get('data'):
            flash(f'No property found for {address}', 'warning')
            return redirect('/')
        
        db_data = Property.get_data_for_db_from_estated_api(data['data'])

        rent_data = requests.get(rm_rent_estimate_api, headers=rm_rent_estimate_headers, params={"address": db_data['address']}).json()
        print(rent_data)
        
        rent_estimate = rent_data.get('rent') or 0.01 * db_data['price']

        print(rent_estimate)
        db_data['rent_monthly'] = rent_estimate
        new_prop = Property.save_new(db_data)
                    
        new_SP = SavedProperty(save_name=new_prop.address, username="search", property_id=new_prop.id)
        db.session.add(new_SP)
        db.session.commit()
        
        return redirect(url_for('property_edit_page', prop_id=new_prop.id))
        
    return redirect('/')


@app.route('/property/<int:prop_id>')
def property_show(prop_id):
    """  """
    
    prop = Property.query.get_or_404(prop_id)
    prop.saved_state()
    
    prop_changes = session.get(f'prop_changes_id{prop_id}')
    
    if prop_changes:
        for k,v in prop_changes.items():
            setattr(prop, k, v)
            
    if current_user.is_authenticated and prop_changes:
        flash('Some changes have not yet been saved', 'warning')
    
    # print((prop.json or {}).get("address"))
    # form = form_creator()
    
    return render_template('property.html', prop=prop)

    
@app.route('/property/<int:prop_id>/edit', methods=["GET", "POST"])
def property_edit_page(prop_id):
    """  """
    
    prop = Property.query.get_or_404(prop_id)
    prop.saved_state()
    
    prop_changes = session.get(f'prop_changes_id{prop_id}')
    if prop_changes:
        form_defaults = Property(**prop_changes)
    else:
        form_defaults = prop
        
    form = form_creator(PropertyEditForm(obj=form_defaults))
    if request.method == 'GET':
        bad_form_data_property_edit = session.pop('bad_form_data', None)
        if bad_form_data_property_edit:
            form = form_creator(PropertyEditForm(MultiDict(bad_form_data_property_edit)))
            form.validate()
            
        if current_user.is_authenticated and prop_changes:
            flash('Some changes have not yet been saved', 'warning')
        
        return render_template('property-edit.html', form=form, prop=prop)
    
    if form.validate_on_submit():
        form_data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        print('================= ||| =================')
        print(form_data)
        form_data['json'] = prop.json
        save = request.form.get('save')
        save_name = request.form.get('save-name')
        
        if save == 'view':
            if prop.search:
                new_prop = Property.save_new(form_data)
                return redirect(url_for('property_show', prop_id=new_prop.id))
            
            session[f'prop_changes_id{prop_id}'] = form_data
            return redirect(url_for('property_show', prop_id=prop_id))
        
        elif current_user.is_authenticated:
            if save == 'new':
                if save_name:
                    if prop.no_saves:
                        prop.save_changes(form_data)
                    else:
                        new_prop = Property.save_new(form_data)
                        prop_id = new_prop.id
                    
                    new_SP = SavedProperty(save_name=save_name, username=current_user.username, property_id=prop_id)
                    db.session.add(new_SP)
                    db.session.commit()
                    
                    session.pop(f'prop_changes_id{prop.id}', None)
                    
                    flash(f'Property "{new_SP.save_name}" has been saved', "success")
                    return redirect(url_for('property_show', prop_id=prop_id))
                else:
                    flash("Save Name Required", 'danger')
                
            elif save == 'update' and prop.cu_saved:
                session.pop(f'prop_changes_id{prop_id}', None)
                if prop.ou_saved:
                    new_prop = Property.save_new(form_data)
                    prop.cu_saved.property_id = prop_id = new_prop.id
                    db.session.commit()
                else:
                    prop.save_changes(form_data)
                
                return redirect(url_for('property_show', prop_id=prop_id))
            else:
                flash("Invalid Submit", 'danger')
            
        elif save == 'new':
            if save_name:
                if not prop.search:
                    session[f'prop_changes_id{prop.id}'] = form_data
                    
                prop_to_save = {'prop_id': prop_id, 'save_name': save_name, **form_data}
                session['prop_to_save'] = prop_to_save
                
                flash("Login or create an account to save this property", "info")
                return redirect(url_for('login'))
            else:
                flash("Save Name Required", 'danger')
        else:
            flash("Invalid Submit", 'danger')
    
    session['bad_form_data_property_edit'] = request.form
    return redirect(url_for('property_edit_page', prop_id=prop_id))
    

@app.route('/property/new', methods=["GET", "POST"])
def property_new_page():
    """  """
    
    form = form_creator(PropertyForm())
    if request.method == 'GET':
        bad_form_data_property_new = session.pop('bad_form_data', None)
        if bad_form_data_property_new:
            form = form_creator(PropertyForm(MultiDict(bad_form_data_property_new)))
            form.validate()
        
        return render_template('property-edit.html', form=form)
    
    if form.validate_on_submit():
        form_data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        save = request.form.get('save')
        save_name = request.form.get('save-name')
        
        if save == 'view':
            new_prop = Property.save_new(form_data)
            
            return redirect(url_for('property_show', prop_id=new_prop.id))
        
        elif current_user.is_authenticated:
            if save == 'new':
                if save_name:
                    new_prop = Property.save_new(form_data)
                    
                    new_SP = SavedProperty(save_name=save_name, username=current_user.username, property_id=new_prop.id)
                    db.session.add(new_SP)
                    db.session.commit()
                    
                    flash(f'Property "{new_SP.save_name}" has been saved', "success")
                    return redirect(url_for('property_show', prop_id=new_prop.id))
                else:
                    flash("Save Name Required", 'danger')  
            else:
                flash("Invalid Submit", 'danger')
            
        elif save == 'new':
            if save_name:
                prop_to_save = {'save_name': save_name, **form_data}
                session['prop_to_save'] = prop_to_save
                
                flash("Login or create an account to save this property", "info")
                return redirect(url_for('login'))
            else:
                flash("Save Name Required", 'danger')
        else:
            flash("Invalid Submit", 'danger')
            
    session['bad_form_data_property_new'] = request.form
    return redirect(url_for('property_new_page'))


# @login_required
# @app.route('/property/compare')
    
@app.route('/user')
@login_required
def user_page():
    """  """
    
    if not current_user.is_authenticated:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    return render_template('user.html')
    

@app.route('/user/edit', methods=["GET", "POST"])
def user_edit():
    """  """
    
    if not current_user.is_authenticated:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = User.query.get_or_404(current_user.username)
    form = form_creator(UserEditForm(obj=user))
    if form.validate_on_submit():
        # print(form.data)
        # print(user.password)
        
        # print(current_user.username)
        # print(form.data.get('username'))
        
        # if form.data.get('username') != current_user.username:
        #     print(user.__dict__.items())
        #     # create new user
        #     print(current_user.saved_properties)
        
        ## change password ##
        # if User.authenticate(current_user.username, form.password.data)
            
        for k,v in form.data.items():
            if k != "csrf_token" and k != "":
                setattr(user, k, v)
        # print(form.data.username)

        db.session.commit()
        login_user(user)
        
        return redirect('/user')
        
    return render_template('user-edit.html', form=form)
    

@app.route('/user/delete', methods=["POST"])
def user_delete():
    """Delete user."""

    if not current_user.is_authenticated:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    db.session.delete(current_user)
    db.session.commit()
    
    logout_user()

    return redirect("/")

@app.route('/user/saved-properties', methods=["GET", "POST"])
@login_required
def user_saved_properties():
    """  """
    
    # saved_props = SavedProperty.query.filter_by(username=current_user.username).all()
    saved_props = current_user.saved_properties
    
    if request.form:
        bro = [v for v in request.form.values()]
        print('================= ||| =================')
        print(bro)
        
    
    # form = form_creator(PropertyCompareForm())
    # if form.validate_on_submit():
    #     form_data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        
    
    return render_template('saved-properties.html', saved_props=saved_props)
    

@app.route('/user/saved-properties/<save_name>/delete', methods=['POST'])
def user_saved_property_delete(save_name):
    """  """
    
    if not current_user.is_authenticated:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    saved_property = SavedProperty.query.get((save_name, current_user.username))
    
    if saved_property:
        session.pop(f'prop_changes_id{saved_property.property_id}', None)
        db.session.delete(saved_property)
        db.session.commit()
    else:
        flash("Invalid Action", 'danger')

    return redirect(url_for('user_saved_properties'))



### To-do ###
# Add user password & username editing
# 

### Bonus to-do ###
# Add Compare Feature
# Search for address in database first