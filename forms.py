from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, RadioField, SelectField, TextAreaField, PasswordField, HiddenField
from wtforms.validators import InputRequired, Email, Optional, URL, NumberRange, Length
from wtforms_alchemy import model_form_factory
from models import db, User, Property, SavedProperty


BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


def form_creator(form, required=True):
    """ Creates an instance of a from with modifiers added """
    
    # Create red stars for required fields
    for field in form:
        if '*' in field.label.text:
            field.label.text=field.label.text[:-1]
            field.required = required
            
    return form

# def length(min=0, max=100):
#     return Length(min=min, max=max, message='Wrong length')

    
class UserSignupForm(ModelForm):
    class Meta:
        model = User
        include_primary_keys = True
        field_args = {'password': {'validators': [Length(min=6, message='Password must be at least 6 characters long'), InputRequired()]}}
        # password = PasswordField("1Password", validators=[InputRequired()])
        # length_validator = length
        
class UserLoginForm(ModelForm):
    class Meta:
        model = User
        # password = PasswordField("1Password", validators=[InputRequired()])
        only = ['username', 'password']
        unique_validator = None
        # length_validator = length
        
class UserEditForm(ModelForm):
    class Meta:
        model = User
        only = ['email']
        # include_primary_keys = True
        # field_args = {'password': {'validators': [Length(min=6, message='Password must be at least 6 characters long')]}}
        
class PropertySearchForm(ModelForm):
    class Meta:
        model = Property
        only = ['address']
        
class PropertyForm(ModelForm):
    class Meta:
        model = Property
        exclude = ['json']
        # field_args = {'json': HiddenField()}
        
class PropertyEditForm(PropertyForm):
    pass

class PropertyViewForm(PropertyForm):
    pass
    
    
# class PropertyEditForm(PropertyForm):
#     save = RadioField('hi', choices=[('view', 'View Changes'), ('new','Save New'), ('update','Save Changes')])
    
class PropertyCompareForm(ModelForm):
    pass
        

