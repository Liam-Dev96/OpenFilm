from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Episode, Movie, TVShow, User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')


    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password1 = request.form.get('pass1')
        password2 = request.form.get('pass2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('first name must be greater than 1 character.', category='error')
        elif len(first_name) < 2:
            flash('last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password should be longer than 7 characters', category='error')
        else:
            new_user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)           
            flash('Account Created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'GET':
        first_name = current_user.first_name

    return render_template("account.html", user=current_user)

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        email = request.form.get('email')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, old_password):
                if new_password == confirm_password:
                    user.password = generate_password_hash(new_password)
                    db.session.commit()
                    flash('Password changed successfully!', category='success')
                    return redirect(url_for('views.home'))
                else:
                    flash('Passwords do not match.', category='error')
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("change_password.html", user=current_user)

@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email():
    if request.method == 'POST':
        old_email = request.form.get('old_email')
        password = request.form.get('password')
        new_email = request.form.get('new_email')

        user = User.query.filter_by(email=old_email).first()
        if user:
            if check_password_hash(user.password, password):
                user.email = new_email
                db.session.commit()
                flash('Email changed successfully!', category='success')
                return redirect(url_for('views.home'))
        else:
            flash('Email does not exist.', category='error')

    return render_template("change_email.html", user=current_user)


@auth.route('/data_population', methods=['GET', 'POST']) 
def populate_data():
    # Insert statements for movies
    movie1 = Movie(
        movie_title="Inception",
        further_info="A thief who steals corporate secrets through the use of dream-sharing technology.",
        img="static/img/inception.jpg",
        preview="https://www.youtube.com/embed/YoHD9XEInc0?si=LVM1pkozoiTt3n_Z",
        full_content="inception_full.mp4",
        imdb_title="tt1375666",
        review="Excellent movie with mind-bending plot.",
        genre="Sci-Fi",
        mov_price=9.99
    )

    movie2 = Movie(
        movie_title="The Matrix",
        further_info="A computer hacker learns about the true nature of his reality and his role in the war against its controllers.",
        img="static/img/matrix.jpg",
        preview="https://www.youtube.com/embed/vKQi3bBA1y8?si=3pZpK7iUZAFx_VZz",
        full_content="matrix_full.mp4",
        imdb_title="tt0133093",
        review="A revolutionary sci-fi movie.",
        genre="Action",
        mov_price=8.99
    )

    movie3 = Movie(
    movie_title="Interstellar",
    further_info="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
    img="static/img/interstellar.jpg",
    preview="https://www.youtube.com/embed/zSWdZVtXT7E?si=3pZpK7iUZAFx_VZz",
    full_content="interstellar_full.mp4",
    imdb_title="tt0816692",
    review="A visually stunning and thought-provoking sci-fi film.",
    genre="Sci-Fi",
    mov_price=10.99
    )

    movie4 = Movie(
        movie_title="The Dark Knight",
        further_info="When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.",
        img="static/img/dark_knight.jpg",
        preview="https://www.youtube.com/embed/EXeTwQWrcwY?si=3pZpK7iUZAFx_VZz",
        full_content="dark_knight_full.mp4",
        imdb_title="tt0468569",
        review="A gripping and intense superhero film.",
        genre="Action",
        mov_price=9.49
    )

    movie5 = Movie(
        movie_title="Pulp Fiction",
        further_info="The lives of two mob hitmen, a boxer, a gangster's wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
        img="static/img/pulp_fiction.jpg",
        preview="https://www.youtube.com/embed/s7EdQ4FqbhY?si=3pZpK7iUZAFx_VZz",
        full_content="pulp_fiction_full.mp4",
        imdb_title="tt0110912",
        review="A classic film with a unique narrative structure.",
        genre="Crime",
        mov_price=7.99
    )

    movie6 = Movie(
    movie_title="The Conjuring",
    further_info="Paranormal investigators Ed and Lorraine Warren work to help a family terrorized by a dark presence in their farmhouse.",
    img="static/img/conjuring.jpg",
    preview="https://www.youtube.com/embed/k10ETZ41q5o?si=3pZpK7iUZAFx_VZz",
    full_content="conjuring_full.mp4",
    imdb_title="tt1457767",
    review="A chilling and well-crafted horror film.",
    genre="Horror",
    mov_price=7.99
    )

    movie7 = Movie(
    movie_title="Superbad",
    further_info="Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-soaked party goes awry.",
    img="static/img/superbad.jpg",
    preview="https://www.youtube.com/embed/MNpoTxeydiY?si=3pZpK7iUZAFx_VZz",
    full_content="superbad_full.mp4",
    imdb_title="tt0829482",
    review="A hilarious and raunchy coming-of-age comedy.",
    genre="Comedy",
    mov_price=6.99
    )


    # Insert statements for TV shows
    tv_show1 = TVShow(
    title="Breaking Bad",
    genre="Drama",
    img="static/img/breaking_bad.jpg",
    description="A high school chemistry teacher turned methamphetamine producer.",
    release_year=2008,
    language="English",
    num_seasons="5",
    num_episodes="62",
    preview="https://www.youtube.com/embed/HhesaQXLuRY?si=ZFjnyIv72VGDpu7I",
    full_content="breaking_bad_full.mp4",
    imdb_title="tt0903747",
    review="One of the best TV shows ever made."
    )

    tv_show2 = TVShow(
    title="Game of Thrones",
    genre="Action",
    img="static/img/game_of_thrones.jpg",
    description="Nine noble families fight for control over the lands of Westeros.",
    release_year=2011,
    language="English",
    num_seasons="8",
    num_episodes="73",
    preview="https://www.youtube.com/embed/bjqEWgDVPe0?si=hAAO4kr4F_hiHk8g",
    full_content="game_of_thrones_full.mp4",
    imdb_title="tt0944947",
    review="Epic fantasy series with complex characters."
    )

    tv_show3 = TVShow(
    title="Stranger Things",
    genre="Horror",
    img="static/img/stranger_things.jpg",
    description="When a young boy disappears, his mother, a police chief, and his friends must confront terrifying supernatural forces.",
    release_year=2016,
    language="English",
    num_seasons="4",
    num_episodes="34",
    preview="https://www.youtube.com/embed/mnd7sFt5c3A?si=3pZpK7iUZAFx_VZz",
    full_content="stranger_things_full.mp4",
    imdb_title="tt4574334",
    review="A thrilling and nostalgic sci-fi series."
    )

    tv_show4 = TVShow(
    title="The Office",
    genre="Comedy",
    img="static/img/the_office.jpg",
    description="A mockumentary on a group of typical office workers, where the workday consists of ego clashes, inappropriate behavior, and tedium.",
    release_year=2005,
    language="English",
    num_seasons="9",
    num_episodes="201",
    preview="https://www.youtube.com/embed/4IvNx2XomI8?si=3pZpK7iUZAFx_VZz",
    full_content="the_office_full.mp4",
    imdb_title="tt0386676",
    review="A hilarious and relatable workplace comedy."
    )

    tv_show5 = TVShow(
        title="Friends",
        genre="Comedy",
        img="static/img/friends.jpg",
        description="Follows the personal and professional lives of six twenty to thirty-something-year-old friends living in Manhattan.",
        release_year=1994,
        language="English",
        num_seasons="10",
        num_episodes="236",
        preview="https://www.youtube.com/embed/hDNNmeeJs1Q?si=3pZpK7iUZAFx_VZz",
        full_content="friends_full.mp4",
        imdb_title="tt0108778",
        review="A beloved and iconic sitcom."
    )
    
    tv_show7 = TVShow(
    title="The Witcher",
    genre="Action",
    img="static/img/witcher.jpg",
    description="Geralt of Rivia, a solitary monster hunter, struggles to find his place in a world where people often prove more wicked than beasts.",
    release_year=2019,
    language="English",
    num_seasons="2",
    num_episodes="16",
    preview="https://www.youtube.com/embed/ndl1W4ltcmg?si=3pZpK7iUZAFx_VZz",
    full_content="witcher_full.mp4",    
    imdb_title="tt5180504",
    review=""
    )

    tv_show8 = TVShow(
    title="The Haunting of Hill House",
    genre="Horror",
    img="static/img/haunting_hill_house.jpg",
    description="Flashing between past and present, a fractured family confronts haunting memories of their old home and the terrifying events that drove them from it.",
    release_year=2018,
    language="English",
    num_seasons="1",
    num_episodes="10",
    preview="https://www.youtube.com/embed/G9OzG53VwIk?si=3pZpK7iUZAFx_VZz",
    full_content="haunting_hill_house_full.mp4",
    imdb_title="tt6763664",
    review="A chilling and emotionally gripping horror series."
    )

    movie8 = Movie(
        movie_title="Dead Silence",
        further_info="After his wife meets a grisly end, Jamie Ashen returns to his haunted hometown of Ravens Fair to find answers. His investigation leads him to the ghost of a ventriloquist named Mary Shaw",
        img="static/img/dead_silence.jpg",
        preview="https://www.youtube.com/embed/8b_HVtHmK30?si=zj5SZm6fLJv0VZF6",
        full_content="dead_silence_full.mp4",
        imdb_title="tt0455760",
        review="A dark and thrilling movie.",
        genre="Horror",
        mov_price=9.99
    )


    movie9 = Movie(
    movie_title="The Hangover",
    further_info="Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing.",
    img="static/img/the_hangover.jpg",
    preview="https://www.youtube.com/embed/tcdUhdOlz9M?si=3pZpK7iUZAFx_VZz",
    full_content="the_hangover_full.mp4",
    imdb_title="tt1119646",
    review="Hilarious and outrageous comedy.",
    genre="Comedy",
    mov_price=9.99
    )

    # Insert statements for TV show episodes
    episodes = [
        Episode(tv_id=1, show_id=1, ep_title="Pilot", img="./static/img/breaking_bad.jpg", description="Walter White turns to a life of crime.", release_year=2008, language="English", season_no="1", episode_no="1", preview="https://www.youtube.com/embed/HhesaQXLuRY", full_content="breaking_bad_ep1.mp4"),
        Episode(tv_id=1, show_id=1, ep_title="Cat's in the Bag...", img="./static/img/breaking_bad.jpg", description="Walt and Jesse attempt to tie up loose ends.", release_year=2008, language="English", season_no="1", episode_no="2", preview="https://www.youtube.com/embed/HhesaQXLuRY", full_content="breaking_bad_ep2.mp4"),
        Episode(tv_id=1, show_id=1, ep_title="...And the Bag's in the River", img="./static/img/breaking_bad.jpg", description="Walt and Jesse clean up the mess.", release_year=2008, language="English", season_no="1", episode_no="3", preview="https://www.youtube.com/embed/HhesaQXLuRY", full_content="breaking_bad_ep3.mp4"),
        Episode(tv_id=1, show_id=1, ep_title="Cancer Man", img="./static/img/breaking_bad.jpg", description="Walt reveals his diagnosis.", release_year=2008, language="English", season_no="1", episode_no="4", preview="https://www.youtube.com/embed/HhesaQXLuRY", full_content="breaking_bad_ep4.mp4"),

        Episode(tv_id=2, show_id=2, ep_title="Winter Is Coming", img="static/img/game_of_thrones.jpg", description="Eddard Stark is torn between his family and an old friend.", release_year=2011, language="English", season_no="1", episode_no="1", preview="https://www.youtube.com/embed/bjqEWgDVPe0", full_content="game_of_thrones_ep1.mp4"),
        Episode(tv_id=2, show_id=2, ep_title="The Kingsroad", img="static/img/game_of_thrones.jpg", description="The Lannisters plot to ensure Bran's silence.", release_year=2011, language="English", season_no="1", episode_no="2", preview="https://www.youtube.com/embed/bjqEWgDVPe0", full_content="game_of_thrones_ep2.mp4"),
        Episode(tv_id=2, show_id=2, ep_title="Lord Snow", img="static/img/game_of_thrones.jpg", description="Jon Snow tries to find his place at the Wall.", release_year=2011, language="English", season_no="1", episode_no="3", preview="https://www.youtube.com/embed/bjqEWgDVPe0", full_content="game_of_thrones_ep3.mp4"),
        Episode(tv_id=2, show_id=2, ep_title="Cripples, Bastards, and Broken Things", img="static/img/game_of_thrones.jpg", description="Ned probes Arryn's death.", release_year=2011, language="English", season_no="1", episode_no="4", preview="https://www.youtube.com/embed/bjqEWgDVPe0", full_content="game_of_thrones_ep4.mp4"),

        Episode(tv_id=3, show_id=3, ep_title="Chapter One: The Vanishing of Will Byers", img="static/img/stranger_things.jpg", description="A young boy vanishes.", release_year=2016, language="English", season_no="1", episode_no="1", preview="https://www.youtube.com/embed/mnd7sFt5c3A", full_content="stranger_things_ep1.mp4"),
        Episode(tv_id=3, show_id=3, ep_title="Chapter Two: The Weirdo on Maple Street", img="static/img/stranger_things.jpg", description="Lucas, Mike, and Dustin try to talk to the girl they found.", release_year=2016, language="English", season_no="1", episode_no="2", preview="https://www.youtube.com/embed/mnd7sFt5c3A", full_content="stranger_things_ep2.mp4"),
        Episode(tv_id=3, show_id=3, ep_title="Chapter Three: Holly, Jolly", img="static/img/stranger_things.jpg", description="An increasingly concerned Nancy looks for Barb.", release_year=2016, language="English", season_no="1", episode_no="3", preview="https://www.youtube.com/embed/mnd7sFt5c3A", full_content="stranger_things_ep3.mp4"),
        Episode(tv_id=3, show_id=3, ep_title="Chapter Four: The Body", img="static/img/stranger_things.jpg", description="Refusing to believe Will is dead, Joyce tries to connect with her son.", release_year=2016, language="English", season_no="1", episode_no="4", preview="https://www.youtube.com/embed/mnd7sFt5c3A", full_content="stranger_things_ep4.mp4"),

        Episode(tv_id=4, show_id=4, ep_title="Pilot", img="static/img/the_office.jpg", description="A documentary crew films the everyday lives of employees.", release_year=2005, language="English", season_no="1", episode_no="1", preview="https://www.youtube.com/embed/4IvNx2XomI8", full_content="the_office_ep1.mp4"),
        Episode(tv_id=4, show_id=4, ep_title="Diversity Day", img="static/img/the_office.jpg", description="Michael's off-color remark puts a sensitivity trainer in the office.", release_year=2005, language="English", season_no="1", episode_no="2", preview="https://www.youtube.com/embed/4IvNx2XomI8", full_content="the_office_ep2.mp4"),
        Episode(tv_id=4, show_id=4, ep_title="Health Care", img="static/img/the_office.jpg", description="Michael lets Dwight choose the new health care plan.", release_year=2005, language="English", season_no="1", episode_no="3", preview="https://www.youtube.com/embed/4IvNx2XomI8", full_content="the_office_ep3.mp4"),
        Episode(tv_id=4, show_id=4, ep_title="The Alliance", img="static/img/the_office.jpg", description="Michael arranges a morale-boosting birthday party.", release_year=2005, language="English", season_no="1", episode_no="4", preview="https://www.youtube.com/embed/4IvNx2XomI8", full_content="the_office_ep4.mp4"),

        Episode(tv_id=5, show_id=5, ep_title="The One Where Monica Gets a Roommate", img="static/img/friends.jpg", description="Rachel runs from her wedding and bumps into her old friend Monica.", release_year=1994, language="English", season_no="1", episode_no="1", preview="https://www.youtube.com/embed/hDNNmeeJs1Q", full_content="friends_ep1.mp4"),
        Episode(tv_id=5, show_id=5, ep_title="The One with the Sonogram at the End", img="static/img/friends.jpg", description="Ross finds out his ex-wife is pregnant.", release_year=1994, language="English", season_no="1", episode_no="2", preview="https://www.youtube.com/embed/hDNNmeeJs1Q", full_content="friends_ep2.mp4"),
        Episode(tv_id=5, show_id=5, ep_title="The One with the Thumb", img="static/img/friends.jpg", description="Monica becomes irritated with her new boyfriend's quirks.", release_year=1994, language="English", season_no="1", episode_no="3", preview="https://www.youtube.com/embed/hDNNmeeJs1Q", full_content="friends_ep3.mp4"),
        Episode(tv_id=5, show_id=5, ep_title="The One with George Stephanopoulos", img="static/img/friends.jpg", description="The girls spy on George Stephanopoulos.", release_year=1994, language="English", season_no="1", episode_no="4", preview="https://www.youtube.com/embed/hDNNmeeJs1Q", full_content="friends_ep4.mp4")
    ]

    # Add episodes to session
    for episode in episodes:
        db.session.add(episode)

    # Add to session and commit to database
    db.session.add(movie1)
    db.session.add(movie2)
    db.session.add(movie3)
    db.session.add(movie4)
    db.session.add(movie5)
    db.session.add(movie6)
    db.session.add(movie7)
    db.session.add(movie8)
    db.session.add(movie9)
    db.session.add(tv_show1)
    db.session.add(tv_show2)
    db.session.add(tv_show3)
    db.session.add(tv_show4)
    db.session.add(tv_show5)
    db.session.add(tv_show7)
    db.session.add(tv_show8)
    db.session.commit()
    flash('Data populated!', category='success')

    return redirect(url_for('views.home'))




    
