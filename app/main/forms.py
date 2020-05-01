from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, DateTimeField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User


class EditProfileForm(FlaskForm):
    first_name = StringField(_l('First Name'), validators=[DataRequired()])
    last_name = StringField(_l('Last Name'), validators=[DataRequired()])
    username = StringField(_l('Username'), validators=[DataRequired()])
    u_email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    u_phone = IntegerField(_l('Phone Number (+852)'), validators=[DataRequired()])
    u_person = RadioField(_l('Social Role'), choices=[('Elderly', _l('Elderly')), ('Adult', _l('Adult')),
                                                      ('Student', _l('Student'))])
    submit = SubmitField(_l('Submit'))

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
    r_category = RadioField(_l('Category'), choices=[('Ticket', _l('Ticket')), ('Staff', _l('Staff')),
                                                     ('Facility', _l('Facility')), ('Website', _l('Website')),
                                                     ('Other', _l('Other'))])
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


class TicketForm(FlaskForm):
    c_num = IntegerField(_l('Cinemas No.'), validators=[DataRequired()])
    m_num = IntegerField(_l('Movie No.'), validators=[DataRequired()])
    p_person = IntegerField(_l('No. of People'), validators=[DataRequired(), Length(min=1)])
    p_role = RadioField(_l('Social Role'), choices=[('Elderly', _l('Elderly')), ('Adult', _l('Adult')),
                                                    ('Student', _l('Student'))])
    t_date = DateTimeField(_l('Date and Time'), format=[format('LLL')], validators=[DataRequired()])
    t_payment = RadioField(_l('Payment'), choices=[('visa', _l('VISA')), ('mastercard', _l('MasterCard'))])
    p_price = IntegerField(_l('Price'), render_kw={'readonly': True})
    submit = SubmitField(_l('Submit'))

    def cal_price(self, p_price, p_person, p_role):
        if p_role.data is 'Elderly':
            p_price = 65
        elif p_role.data is 'Adult':
            p_price = 75
        elif p_role.data is 'Student':
            p_price = 55
        return p_price * p_person