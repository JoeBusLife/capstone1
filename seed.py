from app import app
from models import db, User, Property, SavedProperty
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db.drop_all()
db.create_all()

pass1 = "yoyoyo"
# p1 = bcrypt.generate_password_hash("yoyoyo").decode("utf8")
pass2 = pass1
pass3 = pass1

u1 = User(
    username="cherry",
    password=pass1,
    email="CherryBoy@hotmail.com",
    # first_name="Sally",
    # last_name="Brock"
)

u2 = User(
    username="Cold",
    password=pass2,
    email="brewskis@yahoo.com",
    # first_name="Chad",
    # last_name="Sizzler"
)

u3 = User(
    username="EtbrickKid",
    password=pass3,
    email="allalone@gmail.com",
)

db.session.add_all([u1, u2, u3])
db.session.commit()


p1 = Property(
    address="7433 Brimway Ln, Reading, PA, 19606",
    price=296000,
    rent_monthly=1600,
    units=1,
    taxes_yearly=4715,
    utilities_yearly=0,
    insurance_yearly=1800,
    property_managment=8,
    repair_maintenance=5,
    closing_costs=9000
    # down_payment=,
    # loan_rate=,
    # vacancy_rate=,
    # hoa_fees=,
    # other_expenses=
)

p2 = Property(
    address="522 Birch St, Reading, PA, 19606",
    price=99000,
    rent_monthly=1295,
    units=2,
    taxes_yearly=1147,
    utilities_yearly=1440,
    insurance_yearly=480,
    property_managment=10,
    repair_maintenance=10,
    closing_costs=7740.26,
    down_payment=25,
    loan_rate=4.75
    # vacancy_rate=,
    # hoa_fees=,
    # other_expenses=
)

p3 = Property(
    address="933 Upper Way, Intercourse, PA, 19756",
    price=1000000,
    rent_monthly=6500,
    units=1,
    taxes_yearly=11000,
    utilities_yearly=0,
    insurance_yearly=3600,
    property_managment=8,
    # repair_maintenance=10,
    closing_costs=40000,
    # down_payment=20,
    loan_rate=3,
    vacancy_rate=6,
    hoa_fees=1320,
    other_expenses=960
)

db.session.add_all([p1, p2, p3])
db.session.commit()


sp1 = SavedProperty(
    save_name="Money Pit",
    username="cherry",
    property_id="1",
)

sp2 = SavedProperty(
    save_name="Inlaw Suite (expensive)",
    username="Cold",
    property_id="1",
)

sp3 = SavedProperty(
    save_name="Big Money",
    username="cherry",
    property_id="3",
)

sp4 = SavedProperty(
    save_name="Good 2 unit",
    username="cherry",
    property_id="2",
)

sp5 = SavedProperty(
    save_name="Mansion $$",
    username="Cold",
    property_id="3",
)

sp6 = SavedProperty(
    save_name="2 unit Bad Neighborhood",
    username="EtbrickKid",
    property_id="2",
)

db.session.add_all([sp1, sp2, sp3, sp4, sp5, sp6])
db.session.commit()
