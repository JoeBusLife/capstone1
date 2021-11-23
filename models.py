"""Models for Cupcake app."""
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import EmailType, PasswordType
from flask_bcrypt import Bcrypt
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import validates
from wtforms import PasswordField
from flask_login import UserMixin, current_user

from helpers import *

from sqlalchemy_defaults import Column, make_lazy_configured

from wtforms.validators import InputRequired, Email, Optional, URL, NumberRange, Length

db = SQLAlchemy()

bcrypt = Bcrypt()

make_lazy_configured(db.mapper)

def connect_db(app):
    db.app = app
    db.init_app(app)
    

class User(UserMixin, db.Model):
    __lazy_options__ = {}
    __tablename__ = 'users'
    
    username = Column(db.String(20),
                        label=u'Username*',
                        primary_key=True,
                        unique=True)
    
    password = Column(db.String(60),
                        label=u'Password*',
                        info={'form_field_class': PasswordField})
    
    email = Column(EmailType(),
                        label=u'Email*',
                        unique=True,
                        nullable=False)
    
    
    saved_properties = db.relationship('SavedProperty', backref='users', cascade="all, delete-orphan")
    
    properties = db.relationship('Property', secondary='saved_properties', backref='users')
    
    # first_name = db.Column(db.String(30),
    #                         nullable=False)
    
    # last_name = db.Column(db.String(30),
    #                         nullable=False)
    
    
    @classmethod
    def signup(cls, username, password, email):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        
        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_pwd, email=email)
    

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False
    
    def get_id(self):
        return self.username
    
    def __repr__(self):
        u = self
        return f"<username={u.username} email={u.email} password={bool(u.password)}>"
        # first_name={u.first_name} last_name={u.last_name}
    
    
class Property(db.Model):
    __lazy_options__ = {}
    __tablename__ = 'properties'
    
    id = Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    address = Column(db.String(),
                        label=u'Address*',
                        nullable=False)
    
    price = Column(db.Float(),
                        label=u'Purchase Price*',
                        nullable=False)
    
    rent_monthly = Column(db.Float(),
                        label=u'Total Monthly Rent*',
                        nullable=False)
    
    units = Column(db.Float(),
                        label=u'Number of Units',
                        nullable=True)
    
    beds = Column(db.Float(),
                        label=u'Bedrooms',
                        nullable=True)
    
    baths = Column(db.Float(),
                        label=u'Bathrooms',
                        nullable=True)
    
    sqft = Column(db.Float(),
                        label=u'Structure Sqft',
                        nullable=True)
    
    acres = Column(db.Float(),
                        label=u'Land Size in Acres',
                        nullable=True)
    
    taxes_yearly = Column(db.Float(),
                        label=u'Taxes (Yearly)',
                        nullable=True)
    
    utilities_yearly = Column(db.Float(),
                        label=u'Utilities Payed by Owner (Yearly)',
                        nullable=True)
    
    insurance_yearly = Column(db.Float(),
                        label=u'Insurance (Yearly)',
                        nullable=True)
    
    property_managment = Column(db.Float(),
                        label=u'Property Management (As a percent of Rent)',
                        default=10.0,
                        nullable=True)
    
    repair_maintenance = Column(db.Float(),
                        label=u'Repair / Maintenance (As a percent of Rent)',
                        default=5.0,
                        nullable=True)
    
    closing_costs = Column(db.Float(),
                        label=u'Closing Costs',
                        nullable=True)
    
    down_payment = Column(db.Float(),
                        label=u'Down Payment (Percentage)',
                        default=20.0,
                        nullable=True)
    
    loan_rate = Column(db.Float(),
                        label=u'Loan Interest Rate',
                        default=4.0,
                        nullable=True)
    
    vacancy_rate = Column(db.Float(),
                        label=u'Vacancy Rate (Percentage)',
                        default=5.0,
                        nullable=True)
    
    hoa_fees = Column(db.Float(),
                        label=u'HOA Fees (Yearly)',
                        nullable=True)
    
    other_expenses = Column(db.Float(),
                        label=u'Other Expenses (Yearly)',
                        nullable=True)
    
    json = Column(JSON,
                  nullable=True)
    
    
    
    
    saved_properties = db.relationship('SavedProperty', backref='properties', cascade="all, delete-orphan")
    
    
    @classmethod
    def save_new(cls, data):
        ('================= ||| =================')
        print(type(v) for v in data.values())
        new_prop = cls(**data)
        db.session.add(new_prop)
        db.session.commit()

        return new_prop
    
    @classmethod
    def get_data_for_db_from_estated_api(cls, data):
        ('================= ||| =================')
        
        add = data.get('address') or {}
        address = f"{add['formatted_street_address'].title()}, {add['city'].title()}, {add['state']} {add['zip_code']}"
        
        struct = data.get('structure') or {}
        baths = ( (struct.get('baths') or 0) + (0.5 if struct.get('partial_baths_count') else 0) ) or None
        
        db_data = {
            'address': address,
            'price': data.get('valuation').get('value'),
            'taxes_yearly': (data.get('taxes') or [{}])[0].get('amount'),
            'units': struct.get('units_count') or 1,
            'beds': struct.get('beds_count'),
            'baths': baths,
            'sqft': struct.get('total_area_sq_ft'),
            'acres': (data.get('parcel') or {}).get('area_acres'),
            'json': data
        }
        return db_data
    
    # @classmethod
    # def save_prop_after_login(cls, prop_to_save):
    #     prop_id = prop_to_save.pop('prop_id')
    #     save_name = prop_to_save.pop('save_name')
    #     session.pop(f'prop_changes_id{prop_id}', None)
    #     new_prop = Property.save_new(prop_to_save)
    #     SP = SavedProperty(save_name=save_name, username=current_user.username, property_id=new_prop.   id)
    #     flash(f'Property "{SP.save_name}" has been saved', "success")
    #     return new_prop

    
    def save_changes(p, form_data):
        for k,v in form_data.items():
            setattr(p, k, v)
        db.session.commit()
        
    
    def saved_state(p):
        p.search = p.cu_saved = p.ou_saved = p.no_saves = False
        saved_props = p.saved_properties
        if saved_props:
            for sp in saved_props:
                if sp.username == 'search':
                    p.search = True
                elif current_user.is_authenticated and sp.username == current_user.username:
                    p.cu_saved = sp
                else:
                    p.ou_saved = True
        else:
            p.no_saves = True
    
    
    def yearly_property_managment(p):
        return p.yearly_rent() * (none_to_0(p.property_managment)/100)
    
    def yearly_repair_maintenance(p):
        return p.yearly_rent() * (none_to_0(p.repair_maintenance)/100)
    
    def yearly_expenses(p):
        return none_to_0(p.taxes_yearly) + none_to_0(p.utilities_yearly) + none_to_0(p.insurance_yearly) + p.yearly_property_managment() + p.yearly_repair_maintenance() + none_to_0(p.hoa_fees) + none_to_0(p.other_expenses)
    
    def yearly_rent(p):
        return p.rent_monthly * 12 * (1 - none_to_0(p.vacancy_rate)/100)
    
    def net_rent(p):
        return p.yearly_rent() - p.yearly_expenses()
    
    def cap_rate(p):
        return p.net_rent() / p.price
    
    
    def __repr__(self):
        p = self
        return f"<Property {p.id} | Address={p.address} | Purchase Price={getattr(p, 'price', 'N/A')} | Units={getattr(p, 'units', 'N/A')}>"



class SavedProperty(db.Model):
    __lazy_options__ = {}
    __tablename__ = 'saved_properties'
    
    save_name = Column(db.String(200),
                        label=u'Save Name (Nickname)',
                        primary_key=True)
    
    username = Column(db.String(20),
                        db.ForeignKey('users.username'),
                        primary_key=True)
    
    property_id = Column(db.Integer,
                        db.ForeignKey('properties.id'))


    def __repr__(self):
        sp = self
        return f"<Save Name={sp.save_name} | Username={sp.username} | Property id={sp.property_id} | Purchase Price={getattr(sp.properties, 'price', 'N/A')} | Units={getattr(sp.properties, 'units', 'N/A')}>"