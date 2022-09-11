#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from sqlalchemy import func
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from jinja2 import Markup
from flask_migrate import Migrate
from datetime import datetime
import os

# #----------------------------------------------------------------------------#
# # App Config.
# #----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)

# # TODO: connect to a local postgresql database

# # Models.
# #----------------------------------------------------------------------------#

from models import *

# #----------------------------------------------------------------------------#
# # Filters.
# #----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


# #  Venues
# #  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  for venue in [venue for venue in Venue.query.all()]:
    # start_time = show.start_time.strftime("%Y-%m-%d %H:%M:%S")
    data=[{
    "city": venue.city,
    "state": venue.state,
    "venues": [{
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": db.session.query(Show).filter(start_time>datetime.now()),}]
      }]
    return render_template('pages/venues.html', areas=data);

        
@app.route('/venues/search', methods=['POST'])
def search_venues():
   search_term=request.form.get('search_term', '')
   search_outcome = db.session.query(Venue).filter(Venue.name.ilike(f'{search_term}%') )
   upcoming_show_query = db.session.query(Show).filter(Show.venue_id==result.id).filter(Show.start_time>datetime.now().all())


   for result in [ outcome for outcome in search_outcome]:
        data = [{
                "id":result.id,
                "name":result.name,
                "num_of_upcoming_shows":len(upcoming_show_query)
                        }]
        response={ 
                "count": len(search_outcome),
                "data": data
              }
   return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  past_show_query = db.session.query(Show).join(Venue).filter(venue_id == venue.id).filter(start_time<datetime.now())
  upcoming_show_query = db.session.query(Show).join(Venue).filter(venue_id ==venue.id).filter(start_time>datetime.now())

  data = {
                "id":  venue.id,
                "name" : venue.name,
                "genres": venue.genres,
                "address": venue.address,
                "city": venue.city,
                "state": venue.state,
                "phone": venue.phone,
                "website_link": venue.website_link,
                "facebook_link": venue.facebook_link,
                "seeking_talent": True,
                "seeking_description": venue.seeking_description,
                "image_link":venue.image_link ,
                "past_shows": past_show_query,
                "upcoming_shows": upcoming_show_query,
                "past_shows_count": len(past_show_query),
                "upcoming_shows_count": len(upcoming_show_query),
                
        }

  return render_template('pages/show_venue.html', venue=data)

# #  Create Venue
# #  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
      name = request.form['name']
      city = request.form['city']
      state = request.form['state']
      address = request.form['address']
      phone = request.form['phone']
      genres = request.form['genres']
      facebook_link = request.form['facebook_link']
      image_link = request.form['image_link']
      website_link = request.form['website_link']
      if "seeking_talent" in request.form:
        seeking_talent =True
      else:
        seeking_talent =False
      seeking_description = request.form['seeking_description']
      venue = Venue(name = name, city = city, state = state, phone = phone, address=address, genres = genres, image_link = image_link, facebook_link = facebook_link, website_link = website_link, seeking_talent=seeking_talent, seeking_description=seeking_description)
      db.session.add(venue)
      db.session.commit()

    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Venue ' + request.form['name']+ ' could not be listed.') 
    else:
         flash('Venue ' + request.form['name'] + ' was successfully listed!')
    finally:
      db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
         venue_record = db.session.query(Venue).filter(venue_id==venue.id).all()  
         db.session.delete(venue_record)
         db.session.commit()
    except:
            db.session.rollback(venue_record)
            flask(f"error,{Venue} record with {venue_id} could not be deleted")
    else:
            flask(f" {Venue} record with {venue_id} was successfully deleted")
    finally:
            db.session.close()

    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    for artist in [db.session.query(Artist).all()]:
                data = [{
                        "artist_id": artist.id,
                        "name": artist.name
                }]
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
   search_term=request.form.get('search_term', '')
   search_outcome = db.session.query(Artist).filter(Artist.name.ilike(f'{search_term}%') )
   upcoming_show_query = db.session.query(Show).filter(Show.venue_id==result.id).filter(Show.start_time>datetime.now().all())


   for result in [ outcome for outcome in search_outcome]:
        data = [{
                "id":result.id,
                "name":result.name,
                "num_of_upcoming_shows":len(upcoming_show_query)
                        }]
        response={ 
                "count": len(search_outcome),
                "data": data
                }

   return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    past_show_query = db.session.query(Show).join(Artist).filter(artist_id ==artist.id).filter(start_time<datetime.now())
    upcoming_show_query = db.session.query(Show).join(Artist).filter(artist_id ==artist.id).filter(start_time>datetime.now())

    data = {
                "id":  venue.id,
                "name" : venue.name,
                "genres": venue.genres,
                "address": venue.address,
                "city": venue.city,
                "state": venue.state,
                "phone": venue.phone,
                "website_link": venue.website_link,
                "facebook_link": venue.facebook_link,
                "seeking_talent": True,
                "seeking_description": venue.seeking_description,
                "image_link":venue.image_link ,
                "past_shows": past_show_query,
                "upcoming_shows": upcoming_show_query,
                "past_shows_count": len(past_show_query),
                "upcoming_shows_count": len(upcoming_show_query),
                
        }

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = ArtistForm(artist_id=form.artist_id.data)
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.image_link.data = artist.image_link
  form.facebook_link.data = artist.facebook_link
  form.website_link.data = artist.website_link
  form.seeking_talent.data =artist.seeking_talent
  form.seeking_description.data = artist.seeking_description

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
   try:
        artist = db.session.query(Artist).filter(artist_id = Artist.id).all()
        artist.name = request.form.get('name')
        artist.city = request.form.get('city')
        artist.state = request.form.get('state')
        artist.phone = request.form.get('phone')
        artist.genres = request.form.getlist('genres')
        artist.image_link = request.form.get('image_link')
        artist.facebook_link = request.form.get('facebook_link')
        artist.website_link = request.form.get('website_link')
        if "seeking_talent" in request.form:
                seeking_talent =True
        else:
            seeking_talent =False
            artist.seeking_description = request.form.get('seeking_description')
            db.session.commit()
   except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred, Artist could not be updated.')  
   else:
        flash('Artist was successfully updated!')
   finally:
          db.session.close()
          

   return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
   form = VenueForm()
   venue = VenueForm(venue_id=form.venue_id.data)
   form.name.data = artist.name
   form.city.data = artist.city
   form.state.data = artist.state
   form.phone.data = artist.phone
   form.genres.data = artist.genres
   form.image_link.data = artist.image_link
   form.facebook_link.data = artist.facebook_link
   form.website_link.data = artist.website_link
   form.seeking_talent.data =artist.seeking_talent
   form.seeking_description.data = artist.seeking_description

   return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
     try:
        venue = db.session.query(Venue).filter(venue_id == Venue.id).all()
        venue.name = request.form.get('name')
        venue.city = request.form.get('city')
        venue.state = request.form.get('state')
        venue.phone = request.form.get('phone')
        venue.genres = request.form.getlist('genres')
        venue.image_link = request.form.get('image_link')
        venue.facebook_link = request.form.get('facebook_link')
        venue.website_link = request.form.get('website_link')
        if "seeking_talent" in request.form:
                seeking_talent =True
        else:
            seeking_talent =False
            venue.seeking_description = request.form.get('seeking_description')
            db.session.commit()
     except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred, Artist could not be updated.')  
     else:
        flash('Artist was successfully updated!')
     finally:
          db.session.close()
     return redirect(url_for('show_venue', venue_id=venue_id))

# #  Create Artist
# #  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        phone = request.form['phone']
        genres = request.form.getlist('genres')
        image_link = request.form['image_link']
        facebook_link = request.form['facebook_link']
        website_link = request.form['website_link']
        if "seeking_venue" in request.form:
            seeking_venue =True
        else:
            seeking_venue =False
        seeking_description = request.form['seeking_description']
        artist = Artist(name = name, city = city, state = state, phone = phone, genres = genres, image_link = image_link, facebook_link = facebook_link, website_link = website_link, seeking_venue=seeking_venue, seeking_description=seeking_description)
        db.session.add(artist)
        db.session.commit()

    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Artist ' + request.form['name']+ ' could not be listed.') 
    else:
         flash('Artist ' + request.form['name'] + ' was successfully listed!')
    finally:
      db.session.close()
    return render_template('pages/home.html')


# #  Shows
# #  ----------------------------------------------------------------

@app.route('/shows')
def shows():
   for show in [shows for shows in Show.query.all()]:
    data=[{
   
      "venue_id": show.venue_id,
      "artist_id" : show.artist_id,
      "start_time": show.start_time
      }]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
#   # called to create new shows in the db, upon submitting new show listing form
#   # TODO: insert form data as a new Show record in the db, instead
    artist_id= request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']
    show = Show(artist_id = artist_id, venue_id = venue_id, start_time = start_time)
    db.session.add(show)
    db.session.commit()
    db.session.close()
#   # on successful db insert, flash success
#   flash('Show was successfully listed!')
#   # TODO: on unsuccessful db insert, flash an error instead.
#   # e.g., flash('An error occurred. Show could not be listed.')
#   # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    # try:
    #   artist_id= request.form['artist_id']
    #   venue_id = request.form['venue_id']
    #   start_time = request.form['start_time']
    #   show = Show(artist_id = artist_id, venue_id = venue_id, start_time = start_time)
    #   db.session.add(show)
    #   db.session.commit()

    # except:
    #   db.session.rollback()
    #   print(sys.exc_info())
    #   flash('An error occurred. Show could not be listed.') 
    # else:
    #      flash('Show was successfully listed!')
    # finally:
    #   db.session.close()
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# # Or specify port manually:
# '''
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port) 
# '''

















