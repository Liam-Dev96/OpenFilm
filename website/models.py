from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


 #model for categories/genres
class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)

#model for movies that are coming soon
class ComingSoon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    title = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    language = db.Column(db.String(15), nullable=False)
    duration = db.Column(db.String(8), nullable=False)
    preview = db.Column(db.String(100), nullable=False)

#model for tv show episodes
class Episode(db.Model):
    ep_id = db.Column(db.Integer, primary_key=True)
    tv_id = db.Column(db.Integer, db.ForeignKey('tv_show.tv_id'))
    show_id = db.Column(db.Integer, db.ForeignKey('tv_show.tv_id'))
    ep_title = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    language = db.Column(db.String(15), nullable=False)
    season_no = db.Column(db.String(20), nullable=False)
    episode_no = db.Column(db.String(20), nullable=False)
    preview = db.Column(db.String(100), nullable=False)
    full_content = db.Column(db.String(100), nullable=False)

#model for movies
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(30), nullable=False)
    further_info = db.Column(db.String(500), nullable=False)
    img = db.Column(db.String(30), nullable=False)
    preview = db.Column(db.String(300), nullable=False)
    full_content = db.Column(db.String(100), nullable=False)
    imdb_title = db.Column(db.String(12), nullable=False)
    review = db.Column(db.String(150), nullable=False)
    genre = db.Column(db.String(12), nullable=False)
    mov_price = db.Column(db.Numeric(4, 2), nullable=False)

#model for movie reviews
class MovRev(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    movie_title = db.Column(db.String(60), nullable=False)
    rate = db.Column(db.String(60), nullable=False)
    message = db.Column(db.Text, nullable=False)
    post_date = db.Column(db.DateTime, nullable=False)

#model for tv shows
class TVShow(db.Model):
    tv_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    language = db.Column(db.String(15), nullable=False)
    num_seasons = db.Column(db.String(20), nullable=False)
    num_episodes = db.Column(db.String(20), nullable=False)
    preview = db.Column(db.String(100), nullable=False)
    full_content = db.Column(db.String(100), nullable=False)
    imdb_title = db.Column(db.String(75), nullable=False)
    review = db.Column(db.String(75), nullable=False)

#model for users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, default=func.now())

