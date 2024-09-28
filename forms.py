# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, FileField
from wtforms.validators import DataRequired

class EventForm(FlaskForm):
    name = StringField('Название события', validators=[DataRequired()])
    date = DateField('Дата события', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Сохранить')

class CSVUploadForm(FlaskForm):
    csv_file = FileField('Загрузить CSV', validators=[DataRequired()])
    submit = SubmitField('Загрузить')
