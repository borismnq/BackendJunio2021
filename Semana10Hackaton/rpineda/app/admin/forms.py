from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField, BooleanField, IntegerField)
from wtforms.validators import DataRequired, Length


class UserAdminForm(FlaskForm):
    role = IntegerField('Rol', validators=[DataRequired()])
    is_admin = BooleanField('Administrador')
    submit = SubmitField('Guardar')
