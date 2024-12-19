from flask import Blueprint, jsonify, redirect, url_for
from flask import render_template, request, flash
from flask_login import login_required, current_user
from . import db
from .models import *
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def home():
    # Get all movies and TV shows from the database
    movies = Movie.query.all() 
    tv_shows = TVShow.query.all() 

    # Render the home page and pass the movies and tv_shows to the template
    return render_template('home.html', movies=movies, tv_shows=tv_shows, user=current_user)

@views.route('all-movies', methods=['GET'])
@login_required
def all_movies():
    # Get all movies from the database
    movies = Movie.query.all()

    # Render the all-movies page and pass the movies to the template
    return render_template('movies.html', movies=movies, user=current_user)

@views.route('all-tv-shows', methods=['GET'])
@login_required
def all_tv_shows():
    # Get all TV shows from the database
    tv_shows = TVShow.query.all()

    # Render the all-tv-shows page and pass the tv_shows to the template
    return render_template('tv_shows.html', tv_shows=tv_shows, user=current_user)

@views.route('view-movie/<int:id>', methods=['GET'])
@login_required
def view_movie(id):
    # Get the movie from the database
    movie = Movie.query.get(id)

    # Render the view-movie page and pass the movie to the template
    return render_template('view_movie.html', movie=movie, user=current_user)

@views.route('view-tv-show/<int:id>', methods=['GET'])
@login_required
def view_tv_show(id):
    # Get the TV show from the database
    tv_show = TVShow.query.get(id)

    # Render the view-tv-show page and pass the tv_show to the template
    return render_template('view_tv_show.html', tv_show=tv_show, user=current_user)

@views.route('episodes/<int:id>', methods=['GET'])
@login_required
def episodes(id):
    # Get the TV show from the database
    episodes = Episode.query.all()
    tv_show = TVShow.query.get(id)
    tv_show_episodes = Episode.query.filter_by(tv_id=id).all()

    # Render the episodes page and pass the tv_show to the template
    return render_template('episodes.html', episode=episodes, tv_show=tv_show, user=current_user)

@views.route('view-episode/<int:tv_id>/<int:ep_id>', methods=['GET'])
@login_required
def view_episode(tv_id, ep_id):
    # Get the episode from the database
    tv_show = TVShow.query.get(tv_id)
    episode = Episode.query.filter_by(ep_id=ep_id, tv_id=tv_id).first()

    return render_template('view_episode.html', episode=episode, episode2=episode, tv_show=tv_show, user=current_user)

@views.route('/delete-account', methods=['GET', 'POST']) 
@login_required 
def delete_account():
    user = User.query.get(current_user.id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Account deleted successfully', category='success')
        return redirect(url_for('auth.sign_up'))
    else:
        flash('Account not found', category='error')
        return redirect(url_for('auth.login'))


# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()
    
#     return jsonify({})
