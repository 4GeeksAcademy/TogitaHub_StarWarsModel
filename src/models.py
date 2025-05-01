from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Float, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    favorite_planets: Mapped[list['Planet']] = relationship(secondary='user_favorite_planets', back_populates='favorited_by')
    favorite_people: Mapped[list['Person']] = relationship(secondary='user_favorite_people', back_populates='favorited_by')


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    diameter: Mapped[float | None] = mapped_column(Float)
    climate: Mapped[str | None] = mapped_column(String(120))
    gravity: Mapped[str | None] = mapped_column(String(120))
    terrain: Mapped[str | None] = mapped_column(String(120))
    surface_water: Mapped[float | None] = mapped_column(Float)
    population: Mapped[float | None] = mapped_column(Float)
    residents: Mapped[list['Person']] = relationship(secondary='planet_residents', back_populates='homeworld')
    favorited_by: Mapped[list['User']] = relationship(secondary='user_favorite_planets', back_populates='favorite_planets')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population,
        }
    
class Person(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    birth_year: Mapped[str | None] = mapped_column(String(20))
    eye_color: Mapped[str | None] = mapped_column(String(20))
    gender: Mapped[str | None] = mapped_column(String(20))
    hair_color: Mapped[str | None] = mapped_column(String(20))
    height: Mapped[float | None] = mapped_column(Float)
    mass: Mapped[float | None] = mapped_column(Float)
    skin_color: Mapped[str | None] = mapped_column(String(20))
    homeworld_id: Mapped[int | None] = mapped_column(ForeignKey('planet.id'))
    homeworld: Mapped['Planet | None'] = relationship(back_populates='residents')
    vehicles: Mapped[list['Vehicle']] = relationship(secondary='vehicle_pilots', back_populates='pilots')
    favorited_by: Mapped[list['User']] = relationship(secondary='user_favorite_people', back_populates='favorite_people')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "homeworld_id": self.homeworld_id,
        }
    
class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    model: Mapped[str | None] = mapped_column(String(120))
    manufacturer: Mapped[str | None] = mapped_column(String(120))
    cost_in_credits: Mapped[float | None] = mapped_column(Float)
    length: Mapped[float | None] = mapped_column(Float)
    max_atmosphering_speed: Mapped[float | None] = mapped_column(Float)
    crew: Mapped[int | None] = mapped_column(Integer)
    passengers: Mapped[int | None] = mapped_column(Integer)
    cargo_capacity: Mapped[float | None] = mapped_column(Float)
    consumables: Mapped[str | None] = mapped_column(String(120))
    vehicle_class: Mapped[str | None] = mapped_column(String(120))
    pilots: Mapped[list['Person']] = relationship(secondary='vehicle_pilots', back_populates='vehicles')
    favorited_by: Mapped[list['User']] = relationship(secondary='user_favorite_vehicles', back_populates='favorite_vehicles')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "passengers": self.passengers,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "vehicle_class": self.vehicle_class,
        }
    
planet_residents = db.Table('planet_residents',
    db.Column('planet_id', Integer, ForeignKey('planet.id'), primary_key=True),
    db.Column('person_id', Integer, ForeignKey('person.id'), primary_key=True)
)

vehicle_pilots = db.Table('vehicle_pilots',
    db.Column('vehicle_id', Integer, ForeignKey('vehicle.id'), primary_key=True),
    db.Column('person_id', Integer, ForeignKey('person.id'), primary_key=True)
)

user_favorite_planets = db.Table('user_favorite_planets',
    db.Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    db.Column('planet_id', Integer, ForeignKey('planet.id'), primary_key=True)
)

user_favorite_people = db.Table('user_favorite_people',
    db.Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    db.Column('person_id', Integer, ForeignKey('person.id'), primary_key=True)
)

user_favorite_vehicles = db.Table('user_favorite_vehicles',
    db.Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    db.Column('vehicle_id', Integer, ForeignKey('vehicle.id'), primary_key=True)
)