from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField

class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=40)])
    email = StringField('Email', [validators.Length(min=6, max=100)])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.Length(min=6, max=40), 
                                          validators.EqualTo('confirm', message ='Passwords must match')])
    confirm = PasswordField('Confirm password')

class LoginForm(Form):  
    email = StringField('Email', validators=[validators.Length(min=6, max=100)])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.Length(min=6, max=40), 
                                          ])
    
    submit = SubmitField('Login')