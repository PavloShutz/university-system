from flask_bootstrap import SwitchField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Optional


class SignupLoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired()],
        render_kw={'placeholder': 'Your username'}
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired()],
        render_kw={"placeholder": "Your password"}
    )
    remember_me = SwitchField(
        "Remember me",
        validators=[Optional()]
    )
    submit = SubmitField("Log In")
