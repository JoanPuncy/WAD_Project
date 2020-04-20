from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, TextAreaField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User


class EditProfileForm(FlaskForm):
    first_name = StringField(_l('First Name'), validators=[DataRequired()])
    last_name = StringField(_l('Last Name'), validators=[DataRequired()])
    username = StringField(_l('Username'), validators=[DataRequired()])
    u_email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    u_phone = IntegerField(_l('Phone Number (+852)'), validators=[DataRequired()])
    u_person = StringField(_l('Social Role (Elderly, Adult, Student)'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def __init__(self, original_u_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_u_email = original_u_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))

    def validate_email(self, u_email):
        if u_email.data != self.original_u_email:
            user = User.query.filter_by(u_email=self.u_email.data).first()
            if u_email is not None:
                raise ValidationError(_('Please use a different email address.'))


class ReportForm(FlaskForm):
    r_email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    r_phone = IntegerField(_l('Phone Number (+852)'), validators=[DataRequired()])
    r_category = SelectField(_l('Category'), choices=[(_l('Ticket')), (_l('Staff')),
                                                      (_l('Facility')), (_l('Website')), (_l('Other'))])
    r_title = StringField(_l('Title'), validators=[DataRequired()])
    r_body = TextAreaField(_l('Content'), validators=[Length(min=0, max=500)])
    submit = SubmitField(_l('Submit'))


    def validate_email(self, r_email):
        if r_email.data != self.original_u_email:
            user = User.query.filter_by(r_email=self.u_email.data).first()
            if r_email is not None:
                raise ValidationError(_('Please use your account email address.'))

    def validate_phone(self, r_phone):
        if r_phone.data != self.original_u_phone:
            user = User.query.filter_by(r_phone=self.u_phone.data).first()
            if r_phone is not None:
                raise ValidationError(_('Please use your account phone number.'))