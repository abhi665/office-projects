from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()


class Country(db.Model):
    __tablename__ = 'countries'

    country_id = db.Column(UUID(as_uuid=True), primary_key=True)
    country_name = db.Column(db.String())

    def __init__(self, country_id, country_name):
        self.country_id = country_id
        self.country_name = country_name

    def lookup(country_id):
        country = Country.query.filter_by(country_id=country_id).first()
        return country

    def lookupbycname(country_name):
        country = Country.query.filter_by(country_name=country_name).first()
        return country
