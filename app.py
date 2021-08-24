import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
# from sqlalchemy.exc import IntegrityError
# from psycopg2.errors import UniqueViolation

from forms import UserRegisterForm, UserLoginForm, UserEditForm, PropertySearchForm, PropertyForm
from models import db, connect_db, User, Property, SavedProperty

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///property_cat'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def homepage():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """
    form = PropertySearchForm()
    
    for f in form:
        if '*' in f.label.text:
            f.label.text=f.label.text[:-1]
            f.required = False
    
    return render_template('index.html', form=form)

@app.route('/property/<int:id>')
@app.route('/property/<int:id>/edit')
@app.route('/property/search', methods=['POST'])
@app.route('/property/new')

@app.route('/users/new')
@app.route('/users/<username>')
@app.route('/users/<username>/edit')



    # yo = [f for f in form]
    # print(yo[0].label.text)
    # for f in form:
    #     if '*' in f.label.text:
    #         f.label.text=f.label.text[:-1]
    #         f.required = True
            
    # print(yo[0].label.__html__())
    # print(dir(yo[0].label))
    # # print(dir(yo))
    # # print('required' in yo[0][0].field_flags)