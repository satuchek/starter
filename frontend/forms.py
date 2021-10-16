from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, AnyOf, URL

class CastlistForm(Form):
    actor_id = StringField(
        'actor_id'
    )
    movie_id = StringField(
        'movie_id'
    )

class MovieForm(Form):
    title = StringField(
        'title', validators=[DataRequired()]
    )

    image_link = StringField(
        'image_link', validators=[URL()]
    )

    imdb_link = StringField(
        'imdb_link', validators=[URL()]
    )
    release_date = DateField(
        'release_date',
        validators=[DataRequired()],
        default= datetime.today()
    )

    seeking_talent = BooleanField( 'seeking_talent', default=False, false_values=('False', 'false', '') )

    seeking_description = StringField(
        'seeking_description'
    )



class ActorForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )

    age = IntegerField(
        'age', validators=[DataRequired()]
    )

    image_link = StringField(
        'image_link', validators=[URL()]
    )
    gender = SelectField(
        'gender', validators=[DataRequired()],
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Nonbinary', 'Nonbinary'),
        ]
     )
    imdb_link = StringField(
        'imdb_link', validators=[URL()]
     )


    seeking_roles = BooleanField( 'seeking_roles' )

    seeking_description = StringField(
            'seeking_description'
     )

