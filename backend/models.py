# backend/models.py
from datetime import datetime
from extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    age_group = db.Column(db.String(20))
    fitness_level = db.Column(db.String(20))
    fear_of_heights = db.Column(db.Boolean, default=False)
    has_medical_condition = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'age_group': self.age_group,
            'fitness_level': self.fitness_level,
            'fear_of_heights': self.fear_of_heights,
            'has_medical_condition': self.has_medical_condition,
        }


class Attraction(db.Model):
    __tablename__ = 'attractions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    altitude = db.Column(db.Integer)
    difficulty_level = db.Column(db.Integer)
    estimated_time = db.Column(db.Integer)
    safety_level = db.Column(db.String(50))
    image_url = db.Column(db.String(500))
    tips = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'altitude': self.altitude,
            'difficulty_level': self.difficulty_level,
            'estimated_time': self.estimated_time,
            'safety_level': self.safety_level,
            'image_url': self.image_url,
            'tips': self.tips,
        }


class Route(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    difficulty = db.Column(db.String(20))
    estimated_duration = db.Column(db.Integer)
    attractions = db.Column(db.Text)  # JSON
    recommended_for = db.Column(db.String(50))
    cable_car_usage = db.Column(db.String(100))
    image_url = db.Column(db.String(500))

    def to_dict(self):
        import json
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'difficulty': self.difficulty,
            'estimated_duration': self.estimated_duration,
            'attractions': json.loads(self.attractions) if self.attractions else [],
            'recommended_for': self.recommended_for,
            'cable_car_usage': self.cable_car_usage,
            'image_url': self.image_url,
        }


class Explanation(db.Model):
    __tablename__ = 'explanations'

    id = db.Column(db.Integer, primary_key=True)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attractions.id'))
    audience_type = db.Column(db.String(50))
    text_content = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'attraction_id': self.attraction_id,
            'audience_type': self.audience_type,
            'text_content': self.text_content,
        }


class Merchant(db.Model):
    __tablename__ = 'merchants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    location = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    rating = db.Column(db.Float)
    commission_rate = db.Column(db.Float)
    url = db.Column(db.String(500))
    distance_from_center = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'location': self.location,
            'phone': self.phone,
            'rating': self.rating,
            'commission_rate': self.commission_rate,
            'url': self.url,
            'distance_from_center': self.distance_from_center,
        }


class UserCheckIn(db.Model):
    __tablename__ = 'user_checkins'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    attraction_id = db.Column(db.Integer, db.ForeignKey('attractions.id'))
    checked_in_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    rating = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'attraction_id': self.attraction_id,
            'checked_in_at': self.checked_in_at.isoformat(),
            'notes': self.notes,
            'rating': self.rating,
        }
