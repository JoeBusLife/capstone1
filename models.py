"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import EmailType, PasswordType
from flask_bcrypt import Bcrypt
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.orm import validates
from wtforms import PasswordField

from sqlalchemy_defaults import Column, make_lazy_configured

from wtforms.validators import InputRequired, Email, Optional, URL, NumberRange, Length

db = SQLAlchemy()

bcrypt = Bcrypt()

make_lazy_configured(db.mapper)

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __lazy_options__ = {}
    __tablename__ = 'users'
    
    username = Column(db.String(20),
                        label=u'Username*',
                        primary_key=True)
    
    password = Column(db.String(60),
                        label=u'Password*',
                        info={'form_field_class': PasswordField},
                        nullable=False)
    
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
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

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
    
    # username = Column(db.String(20),
    #                     db.ForeignKey('users.username'))
    
    # save_name = Column(db.String(30),
    #                     label=u'Save Name (Nickname)')
    
    address = Column(db.String(),
                        label=u'Address*')
    
    price = Column(db.Float(),
                        label=u'Purchase Price')
    
    rent_monthly = Column(db.Float(),
                        label=u'Total Monthly Rent')
    
    units = Column(db.Float(),
                        label=u'Number of Units',
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
                        default=10,
                        nullable=True)
    
    repair_maintenance = Column(db.Float(),
                        label=u'Repair / Maintenancey (As a percent of Rent)',
                        default=5,
                        nullable=True)
    
    closing_costs = Column(db.Float(),
                        label=u'Closing Costs',
                        nullable=True)
    
    down_payment = Column(db.Float(),
                        label=u'Down Payment (Percentage)',
                        default=20,
                        nullable=True)
    
    loan_rate = Column(db.Float(),
                        label=u'Loan Interest Rate',
                        default=4,
                        nullable=True)
    
    vacancy_rate = Column(db.Float(),
                        label=u'Vacancy Rate (Percentage)',
                        default=5,
                        nullable=True)
    
    hoa_fees = Column(db.Float(),
                        label=u'HOA Fees (Yearly)',
                        nullable=True)
    
    other_expenses = Column(db.Float(),
                        label=u'Other Expenses (Yearly)',
                        nullable=True)
    
    
    
    
    saved_properties = db.relationship('SavedProperty', backref='properties', cascade="all, delete-orphan")
    
    
    
    # address = db.Column(db.String(),
    #                     nullable=False)
    
    # price = db.Column(db.Integer(),
    #                     nullable=False)
    
    # content = db.Column(db.Text,
    #                     nullable=False)
    
    
    def __repr__(self):
        p = self
        return f"<Property {p.id} Address={p.address} Purchase Price={p.purchase_price} Units={p.number_of_units}>"


class SavedProperty(db.Model):
    __lazy_options__ = {}
    __tablename__ = 'saved_properties'
    
    save_name = Column(db.String(30),
                        label=u'Save Name (Nickname)')
    
    username = Column(db.String(20),
                        db.ForeignKey('users.username'),
                        primary_key=True)
    
    property_id = Column(db.Integer,
                        db.ForeignKey('properties.id'),
                        primary_key=True)


    def __repr__(self):
        sp = self
        return f"<Save Name={sp.save_name} Username={sp.username} Property id={sp.property_id} Purchase Price={sp.properties.purchase_price}>"