from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd

train=pd.read_csv('data/Train.csv')
val=pd.read_csv('data/Val.csv')
X_data=pd.concat([train,val],axis=0).drop(columns="price")

class InputForm(FlaskForm):
    airline=SelectField(
        "Airline",
        validators=[DataRequired()],
        choices=X_data.airline.unique().tolist()
    )
    date_of_journey=DateField(
        "Date of Journey",
        validators=[DataRequired()]
    )
    source=SelectField(
        "Source",
        validators=[DataRequired()],
        choices=X_data.source.unique().tolist()
    )
    destination=SelectField(
        "Destination",
        validators=[DataRequired()],
        choices=X_data.destination.unique().tolist()
    )
    dep_time=TimeField(
        "Departure Time",
        validators=[DataRequired()]
    )
    arr_time=TimeField(
        "Arrival Time",
        validators=[DataRequired()]
    )
    duration=IntegerField(
        "Duration",
        validators=[DataRequired()]
    )
    total_stops=IntegerField(
        "Number of Stops",
        validators=[DataRequired()]
    )
    additional_info=SelectField(
        "Additional Info",
        validators=[DataRequired()],
        choices=X_data.additional_info.unique().tolist()
    )
    predict=SubmitField("Predict")
