from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    powers = relationship('Power', secondary='hero_powers', back_populates='heroes')
    hero_powers = relationship('HeroPower', back_populates='hero')

    def __repr__(self):
        return f'<Hero {self.id}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    heroes = relationship('Hero', secondary='hero_powers', back_populates='powers')
    hero_powers = relationship('HeroPower', back_populates='power')

    @validates('name')
    def validate_name(self, key, name):
        assert name.strip(), "Name must not be empty"
        return name

    def __repr__(self):
        return f'<Power {self.id}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, ForeignKey('powers.id'), nullable=False)

    hero = relationship('Hero', back_populates='hero_powers')
    power = relationship('Power', back_populates='hero_powers')

    @validates('strength')
    def validate_strength(self, key, strength):
        assert strength.strip(), "Strength must not be empty"
        return strength

    def __repr__(self):
        return f'<HeroPower {self.id}>'
