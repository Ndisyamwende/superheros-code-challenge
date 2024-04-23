#!/usr/bin/env python3

from flask import Flask, request, make_response, app, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    data = request.json
    description = data.get('description')

    # Check if the Power exists
    power = Power.query.get(id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404

    # Update the description if provided
    if description:
        power.description = description

    # Validate the updated Power
    errors = power.validate()
    if errors:
        return jsonify({'errors': errors}), 400

    # Commit changes to the database
    db.session.commit()

    # Return updated Power data
    return jsonify({
        'id': power.id,
        'name': power.name,
        'description': power.description
    })


# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')

    # Check if the Power and Hero exist
    power = Power.query.get(power_id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404

    hero = Hero.query.get(hero_id)
    if hero is None:
        return jsonify({'error': 'Hero not found'}), 404

    # Create a new HeroPower
    hero_power = HeroPower(strength=strength, power=power, hero=hero)

    # Validate the new HeroPower
    errors = hero_power.validate()
    if errors:
        return jsonify({'errors': errors}), 400

    # Commit changes to the database
    db.session.add(hero_power)
    db.session.commit()

    # Return data related to the new HeroPower
    return jsonify({
        'id': hero_power.id,
        'hero_id': hero_power.hero_id,
        'power_id': hero_power.power_id,
        'strength': hero_power.strength,
        'hero': {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        },
        'power': {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
    })



if __name__ == '__main__':
    app.run(port=5555, debug=True)
