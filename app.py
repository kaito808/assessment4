"""Blogly application."""

from flask import Flask, redirect, render_template, request, flash, url_for, jsonify
from models import db, connect_db, Pet, Song, Playlist, PlaylistSong
from flask_debugtoolbar import DebugToolbarExtension
from forms import PlaylistForm, NewSongForPlaylistForm, SongForm




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'asdfasdfasdfasd'

app.app_context().push()
connect_db(app)
db.create_all()


toolbar = DebugToolbarExtension(app)

@app.route('/')
def list_pets():
    """List all pets."""

    return redirect("/playlists")
    




@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)

##############################################################################

# @app.route("/api/pets/<int:pet_id>", methods=['GET'])
# def api_get_pet(pet_id):
#     """Return basic info about pet in JSON."""

#     pet = Pet.query.get_or_404(pet_id)
#     info = {"name": pet.name, "age": pet.age}

#     return jsonify(info)

@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""

    playlist = Song.query.get_or_404(playlist_id)
    return render_template("playlist.html", playlist=playlist)

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK



@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """return a specific song"""

    song = Song.query.get_or_404(song_id)
    return render_template("song.html", song=song)


@app.route("/songs/add", methods=["GET","POST"])
def add_song():
    """Handle add-song form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-songs
    """

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK

    form = SongForm()
    

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_song = Song(**data)
        # new_song = Song(name=form.name.data, age=form.age.data, ...)
        db.session.add(new_song)
        db.session.commit()
        # flash(f"{new_song.name} added.")
        return redirect("/songs")


    else:
        return render_template("new_song.html", form=form)



# @app.route('/playlists/<int:playlist_id>/add-song')
# def add_song_to_pl(playlist_id):
   

#     playlist = Playlist.query.get_or_404(playlist_id)
#     songs = Song.query.all()
#     return render_template('add_song_to_playlist.html', songs = songs, playlist=playlist)

# @app.route("/playlists/<int:playlist_id>/add-song", methods=["POST"])
# def add_song_to_playlist(playlist_id):
#     """Add a playlist and redirect to list."""

#     playlist = Playlist.query.get_or_404(playlist_id)
#     playlist.name = request.form['song_id']
#     song_ids = [int(num) for num in request.form.getlist("songs")]
#     playlist.song = Song.query.filter(Song.id.in_(song_ids)).all()
#     songs = Song.query.all()


#     db.session.add(songs)
#     db.session.commit()
#     flash(f"Playlist '{playlist.name}' edited.")

#     return redirect("/playlists")

@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    # Restrict form to songs not already on this playlist

    curr_on_playlist = [s.id for s in playlist.songs]
    form.song.choices = (db.session.query(Song.id, Song.title)
                         .filter(Song.id.notin_(curr_on_playlist))
                         .all())

    if form.validate_on_submit():

        # This is one way you could do this ...
        playlist_song = PlaylistSong(song_id=form.song.data,
                                     playlist_id=playlist_id)
        db.session.add(playlist_song)

        # Here's another way you could that is slightly more ORM-ish:
        #
        # song = Song.query.get(form.song.data)
        # playlist.songs.append(song)

        # Either way, you have to commit:
        db.session.commit()

        return redirect(f"/playlists/{playlist_id}")

    else:
        return render_template("add_song_to_playlist.html",
                               playlist=playlist,
                               form=form)











"""okay for songs"""
@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)

@app.route("/playlists/add", methods=["GET","POST"])
def add_playlist():
    
    form = PlaylistForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_playlist = Playlist(**data)

        db.session.add(new_playlist)
        db.session.commit()
        # flash(f"{new_playlist.name} added.")
        return redirect('/playlists')

    else:
        return render_template("new_playlist.html", form=form)