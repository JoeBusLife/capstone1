from app import app
from models import db, User, Property, SavedProperty
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db.drop_all()
db.create_all()

pass1 = bcrypt.generate_password_hash("yoyoyo").decode("utf8")
pass2 = pass1
pass3 = pass1
pass4 = pass1

u1 = User(
    username="search",
    password=pass1,
    email="Search@APIResults.com",
)

u2 = User(
    username="cherry",
    password=pass1,
    email="CherryBoy@hotmail.com",
    # first_name="Sally",
    # last_name="Brock"
)

u3 = User(
    username="Cold",
    password=pass2,
    email="brewskis@yahoo.com",
    # first_name="Chad",
    # last_name="Sizzler"
)

u4 = User(
    username="EtbrickKid",
    password=pass3,
    email="allalone@gmail.com",
)

db.session.add_all([u1, u2, u3, u4])
db.session.commit()


json5 = {'metadata': {'publishing_date': '2019-07-01'}, 'address': {'street_number': '110', 'street_pre_direction': None, 'street_name': 'OCEAN PARK', 'street_suffix': 'BLVD', 'street_post_direction': None, 'unit_type': 'UNIT', 'unit_number': '205', 'formatted_street_address': '110 OCEAN PARK BLVD UNIT 205', 'city': 'SANTA MONICA', 'state': 'CA', 'zip_code': '90405', 'zip_plus_four_code': '3559', 'carrier_code': 'C032', 'latitude': 34.000893, 'longitude': -118.484675, 'geocoding_accuracy': 'PARCEL CENTROID', 'census_tract': '060377021.021000'}, 'parcel': {'apn_original': '4288-021-072', 'apn_unformatted': '4288021072', 'apn_previous': None, 'fips_code': '06037', 'frontage_ft': None, 'depth_ft': None, 'area_sq_ft': 196170, 'area_acres': 4.503, 'county_name': 'LOS ANGELES', 'county_land_use_code': '010C', 'county_land_use_description': 'SINGLE RESIDENTIAL - CONDOMINIUM', 'standardized_land_use_category': 'RESIDENTIAL', 'standardized_land_use_type': 'CONDOMINIUM UNIT', 'location_descriptions': [], 'zoning': 'SMOP4*', 'building_count': None, 'tax_account_number': None, 'legal_description': 'TR=34110 LOT 4 CONDOMINIUM UNIT 205', 'lot_code': None, 'lot_number': '4', 'subdivision': 'BARNARD WAY SEA COLONY', 'municipality': None, 'section_township_range': None}, 'structure': {'year_built': 1987, 'effective_year_built': None, 'stories': None, 'rooms_count': None, 'beds_count': 1, 'baths': 2.0, 'partial_baths_count': None, 'units_count': 1, 'parking_type': None, 'parking_spaces_count': None, 'pool_type': None, 'architecture_type': None, 'construction_type': None, 'exterior_wall_type': None, 'foundation_type': None, 'roof_material_type': None, 'roof_style_type': None, 'heating_type': 'CENTRAL', 'heating_fuel_type': None, 'air_conditioning_type': 'YES', 'fireplaces': None, 'basement_type': None, 'quality': 'C+', 'condition': None, 'flooring_types': [], 'plumbing_fixtures_count': None, 'interior_wall_type': None, 'water_type': None, 'sewer_type': None, 'total_area_sq_ft': 1146, 'other_areas': [], 'other_rooms': [], 'other_features': [], 'other_improvements': [], 'amenities': []}, 'valuation': {'value': 1074000, 'high': 1278060, 'low': 869940, 'forecast_standard_deviation': 19, 'date': '2020-01-29'}, 'taxes': [{'year': 2019, 'amount': 10187, 'exemptions': [], 'rate_code_area': '8-609'}], 'assessments': [{'year': 2019, 'land_value': 610283, 'improvement_value': 211296, 'total_value': 821579}], 'market_assessments': [], 'owner': {'name': 'MCCAVANA SEAN', 'second_name': None, 'unit_type': 'UNIT', 'unit_number': '205', 'formatted_street_address': '110 OCEAN PARK BLVD', 'city': 'SANTA MONICA', 'state': 'CA', 'zip_code': '90405', 'zip_plus_four_code': '3559', 'owner_occupied': 'YES'}, 'deeds': [{'document_type': 'GRANT DEED', 'recording_date': '2004-09-01', 'original_contract_date': '2004-07-21', 'deed_book': None, 'deed_page': None, 'document_id': '04-2255848', 'sale_price': 657500, 'sale_price_description': 'FULL AMOUNT COMPUTED FROM TRANSFER TAX OR EXCISE TAX', 'transfer_tax': None, 'distressed_sale': False, 'real_estate_owned': 'NO', 'seller_first_name': None, 'seller_last_name': 'WAVE MAKER CORP', 'seller2_first_name': None, 'seller2_last_name': None, 'seller_address': None, 'seller_unit_number': None, 'seller_city': None, 'seller_state': None, 'seller_zip_code': None, 'seller_zip_plus_four_code': None, 'buyer_first_name': 'SEAN', 'buyer_last_name': 'MCCAVANA', 'buyer2_first_name': None, 'buyer2_last_name': None, 'buyer_address': '110 OCEAN PARK BLVD', 'buyer_unit_type': 'UNIT', 'buyer_unit_number': '205', 'buyer_city': 'SANTA MONICA', 'buyer_state': 'CA', 'buyer_zip_code': '90405', 'buyer_zip_plus_four_code': '3559', 'lender_name': 'SECURED BANKERS MORTGAGE CO', 'lender_type': 'MORTGAGE COMPANY', 'loan_amount': 524625, 'loan_type': 'UNKNOWN', 'loan_due_date': '2034-09-01', 'loan_finance_type': 'FIXED RATE', 'loan_interest_rate': 5.65}, {'document_type': 'GRANT DEED', 'recording_date': '2001-07-19', 'original_contract_date': '2001-06-07', 'deed_book': None, 'deed_page': None, 'document_id': '01-1270377', 'sale_price': 370000, 'sale_price_description': 'FULL AMOUNT COMPUTED FROM TRANSFER TAX OR EXCISE TAX', 'transfer_tax': None, 'distressed_sale': False, 'real_estate_owned': 'NO', 'seller_first_name': 'JAMES R', 'seller_last_name': 'SAMPLE', 'seller2_first_name': 'AMY L', 'seller2_last_name': 'SAMPLE', 'seller_address': None, 'seller_unit_number': None, 'seller_city': None, 'seller_state': None, 'seller_zip_code': None, 'seller_zip_plus_four_code': None, 'buyer_first_name': None, 'buyer_last_name': 'WAVE MAKER CORP', 'buyer2_first_name': None, 'buyer2_last_name': None, 'buyer_address': '111 N CENTRAL AVE', 'buyer_unit_type': None, 'buyer_unit_number': None, 'buyer_city': 'HARTSDALE', 'buyer_state': 'NY', 'buyer_zip_code': '10530', 'buyer_zip_plus_four_code': '1903', 'lender_name': 'WASHINGTON MUTUAL BANK FA', 'lender_type': 'BANK', 'loan_amount': 270000, 'loan_type': None, 'loan_due_date': '2031-08-01', 'loan_finance_type': 'ADJUSTABLE RATE', 'loan_interest_rate': 7.12}, {'document_type': 'INTRAFAMILY TRANSFER AND DISSOLUTION', 'recording_date': '1997-08-05', 'original_contract_date': '1997-07-25', 'deed_book': None, 'deed_page': None, 'document_id': '97-1191153', 'sale_price': None, 'sale_price_description': None, 'transfer_tax': None, 'distressed_sale': False, 'real_estate_owned': 'NO', 'seller_first_name': 'JAMES R', 'seller_last_name': 'SAMPLE', 'seller2_first_name': None, 'seller2_last_name': None, 'seller_address': '1708 FILLMORE DR', 'seller_unit_number': None, 'seller_city': 'MONTEREY PARK', 'seller_state': 'CA', 'seller_zip_code': '91755', 'seller_zip_plus_four_code': '4120', 'buyer_first_name': 'JAMES R', 'buyer_last_name': 'SAMPLE', 'buyer2_first_name': 'AMY L', 'buyer2_last_name': 'SAMPLE', 'buyer_address': '1708 FILLMORE DR', 'buyer_unit_type': None, 'buyer_unit_number': None, 'buyer_city': 'MONTEREY PARK', 'buyer_state': 'CA', 'buyer_zip_code': '91755', 'buyer_zip_plus_four_code': '4120', 'lender_name': 'T J FINANCIAL INC', 'lender_type': 'OTHER', 'loan_amount': 201500, 'loan_type': None, 'loan_due_date': '2012-08-01', 'loan_finance_type': None, 'loan_interest_rate': None}]}

p1 = Property(
    address="7433 Brimway Ln, Reading, PA 19606",
    price=296000,
    rent_monthly=1600,
    units=1,
    beds=4,
    baths=2,
    sqft=2338,
    acres=0.35,
    taxes_yearly=4715,
    utilities_yearly=0,
    insurance_yearly=1800,
    property_managment=8,
    repair_maintenance=5,
    closing_costs=9000,
    # down_payment=,
    # loan_rate=,
    # vacancy_rate=,
    # hoa_fees=,
    # other_expenses=,
    # json=
)

p2 = Property(
    address="522 Birch St, Reading, PA 19606",
    price=99000,
    rent_monthly=1295,
    units=2,
    beds=3,
    baths=2,
    sqft=1973,
    # acres=,
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
    # other_expenses=,
    # json=
)

p3 = Property(
    address="933 Upper Way, Intercourse, PA 19756",
    price=1000000,
    rent_monthly=6500,
    units=1,
    beds=7,
    baths=4.5,
    sqft=9200,
    acres=8,
    taxes_yearly=11000,
    utilities_yearly=0,
    insurance_yearly=3600,
    property_managment=8,
    # repair_maintenance=10,
    closing_costs=55000,
    # down_payment=20,
    loan_rate=3,
    vacancy_rate=6,
    hoa_fees=1320,
    other_expenses=960
    # json=
)

p4 = Property(
    address="933 Upper Way, Intercourse, PA 19756",
    price=1000000,
    rent_monthly=7500,
    units=1,
    beds=7,
    baths=4.5,
    sqft=9200,
    acres=8,
    taxes_yearly=11000,
    utilities_yearly=0,
    insurance_yearly=3000,
    property_managment=8,
    # repair_maintenance=10,
    closing_costs=55000,
    # down_payment=20,
    loan_rate=3,
    vacancy_rate=5,
    hoa_fees=1320,
    other_expenses=960
    # json=
)

p5 = Property(
    address="110 Ocean Park Blvd Unit 205, Santa Monica, CA 90405",
    price=1074000,
    rent_monthly=8579.63,
    units=1,
    beds=1,
    baths=2,
    sqft=1146,
    acres=4.503,
    taxes_yearly=10187,
    utilities_yearly=0,
    insurance_yearly=1800,
    property_managment=7,
    repair_maintenance=2,
    closing_costs=66812,
    down_payment=5,
    loan_rate=3,
    vacancy_rate=5,
    hoa_fees=10680,
    other_expenses=0,
    json=json5
)

db.session.add_all([p1, p2, p3, p4, p5])
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

sp7 = SavedProperty(
    save_name="933 Upper Way, Intercourse, PA 19756",
    username="search",
    property_id="4",
)

sp8 = SavedProperty(
    save_name="LA Beach",
    username="cherry",
    property_id="5",
)

db.session.add_all([sp1, sp2, sp3, sp4, sp5, sp6, sp7, sp8])
db.session.commit()
