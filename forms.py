from wtforms import Form, StringField, validators

class Registration_form(Form):
    username = StringField('Username', [validators.Length(min = 3, max = 55)])

