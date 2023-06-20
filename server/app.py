#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal=Animal.query.filter(Animal.id== id).first()
    
    if animal is None:
        return 'animal not found', 404


    
    #back_populate Relationshi 
    zookeeper = animal.zookeeper
    enclosure = animal.enclosure
    
    response_body = f'''
    <ul>ID: {animal.id}</ul>
    <ul>Name: {animal.name}</ul>
    <ul>Species: {animal.species}</ul>
    <ul>Zookeeper: {zookeeper.name}</ul>
    <ul>Enclosure: {enclosure.environment}</ul>
    '''
    response= make_response(response_body,200)
    
    
    
    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper=Zookeeper.query.filter(Zookeeper.id== id).first()
    
    if zookeeper is None:
        return 'Zookeeper not found', 404


    
    #relationship
    animals = zookeeper.animals
    #iterate throu the animals and extract its name and join them
    animal_names = [f'<ul>Animal: {animal.name}</ul>' for animal in zookeeper.animals]
    
     
    response_body=f'''
    <ul>ID:{zookeeper.id}</ul>
    <ul>Name:{zookeeper.name}</ul>
    <ul>Birthday:{zookeeper.birthday}</ul>
     
     {''.join(animal_names)}

    '''
    response= make_response(response_body,200)
    
    return response
    

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure=Enclosure.query.filter(Enclosure.id== id).first()
    
    if enclosure is None:
        return 'enclosure not found', 404
    
    
    #relationship
    animals = enclosure.animals
    #iterate throu the animals and extract its name and join them
    animal_names = [f'<ul>Animal: {animal.name}</ul>' for animal in enclosure.animals]
    

     
    response_body=f'''
    <ul>ID:{enclosure.id}</ul>
    <ul>Environment:{enclosure.environment}</ul>
    <ul>Open_to_visitors:{enclosure.open_to_visitors}</ul>
    
    {''.join(animal_names)}

    '''
    response= make_response(response_body,200)
    
    return response


if __name__ == '__main__':
    app.run(port=5523, debug=True)

