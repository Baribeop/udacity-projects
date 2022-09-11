from app import db
from datetime import datetime

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120),nullable=False)
    state = db.Column(db.String(120),nullable=False)
    address = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.String(120),nullable=False)
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description =db.Column(db.String(500))
    show = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
             return f"<Artist id: {self.id}, name: {self.name} , city: {self.name}, state:{self.state}, address:{self.address}, phone: {self.phone}>"
    # def __repr__(self):
    #     return '<Venue {}>'.format(self.name)
    
    
class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=False)
    city = db.Column(db.String(120),nullable=False)
    state = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String()),nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description =db.Column(db.String(500))
    show = db.relationship('Show', backref='artist', lazy=True)
        
    def __repr__(self):
            return f"<Artist id: {self.id}, name: {self.name} , city: {self.name}, state:{self.state} phone:{self.phone}>"
    # def __repr__(self):
    #     return '<Artist {}>'.format(self.name)

class Show(db.Model):
    __tablename__ = 'shows'
    show_id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'),nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id') ,nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    

  
    def __repr__(self):
            return f"<Show artist_id: {self.artist_id}, venue_id: {self.venue_id}, start_time: {self.start_time}>"
    # def __repr__(self):
    #     return '<Show {}{}>'.format(self.artist_id, self.venue_id)