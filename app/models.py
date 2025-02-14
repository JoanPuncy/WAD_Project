from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = 'cw_user'
    id = db.Column(db.Integer, db.Sequence('cw_user_id_seq'), primary_key=True)
    first_name = db.Column(db.String(100), unique=False)
    last_name = db.Column(db.String(50), unique=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    u_email = db.Column(db.String(150), unique=True, nullable=False)
    u_phone = db.Column(db.Integer, unique=False, nullable=False)
    u_person = db.Column(db.String, unique=False, nullable=False)
    password = db.Column(db.String(100))
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    created_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def avatar(self, size):
        digest = md5(self.u_email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Reports(db.Model):
    __tablename__ = 'cw_reports'
    rid = db.Column(db.Integer, db.Sequence('cw_report_id_seq'), primary_key=True)
    r_email = db.Column(db.String(150), unique=True, nullable=False)
    r_phone = db.Column(db.Integer, unique=False, nullable=False)
    r_category = db.Column(db.String(50))
    r_title = db.Column(db.String(100))
    r_body = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('cw_user.id'))


class Ticket(db.Model):
    __tablename__ = 'cw_ticket'
    tid = db.Column(db.Integer, db.Sequence('cw_ticket_id_seq'), primary_key=True)
    c_num = db.Column(db.Integer, nullable=False)
    m_num = db.Column(db.Integer, nullable=False)
    p_person = db.Column(db.Integer)
    p_role = db.Column(db.String)
    t_date = db.Column(db.DateTime)
    p_price = db.Column(db.Integer)
    t_payment = db.Column(db.String, nullable=False)
    generate_time = db.Column(db.DateTime,  default=datetime.utcnow, nullable=True)
    cid = db.Column(db.Integer, db.ForeignKey('cw_cinemas.cid'))
    mid = db.Column(db.Integer, db.ForeignKey('cw_movie.mid'))
    pid = db.Column(db.Integer, db.ForeignKey('cw_price.pid'))


class Cinemas(db.Model):
    __tablename__ = 'cw_cinemas'
    cid = db.Column(db.Integer, primary_key=True)
    c_num = db.Column(db.Integer, nullable=False, unique=True)
    c_name = db.Column(db.String(50), unique=True)
    c_district = db.Column(db.String(50), unique=False)
    c_address = db.Column(db.String(250), unique=True)
    fid = db.Column(db.Integer, db.ForeignKey('cw_facility.fid'))

    def __repr__(self):
        return '<Cinemas {}>'.format(self.c_name)


class Facility(db.Model):
    __tablename__ = 'cw_facility'
    fid = db.Column(db.Integer, primary_key=True)
    total_house = db.Column(db.Integer, nullable=False)
    total_seat = db.Column(db.Integer, nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey('cw_cinemas.cid'))

    def __repr__(self):
        return '<Cinemas {}>'.format(self.total_house)


class Movie(db.Model):
    __tablename__ = 'cw_movie'
    mid = db.Column(db.Integer, primary_key=True)
    m_num = db.Column(db.Integer, nullable=False, unique=True)
    m_name = db.Column(db.String(100), unique=True)
    m_unreleased = db.Column(db.Boolean, default=False)
    m_type = db.Column(db.String(50))
    m_category = db.Column(db.String(3), nullable=False)
    m_language = db.Column(db.String)
    m_releasedate = db.Column(db.DateTime)

    def __repr__(self):
        return '<Movie {}>'.format(self.m_name)


class M_Category(db.Model):
    __tablename__ = 'cw_m_category'
    mcid = db.Column(db.Integer, primary_key=True)
    mc_level = db.Column(db.String(3), unique=True)
    mc_definition = db.Column(db.String(50))


class Price(db.Model):
    __tablename__ = 'cw_price'
    pid = db.Column(db.Integer, primary_key=True)
    p_role = db.Column(db.String)
    p_person = db.Column(db.Integer)
    p_time = db.Column(db.DateTime)
    p_price = db.Column(db.Integer)


class Contact(db.Model):
    __tablename__ = 'cw_contact'
    conid = db.Column(db.Integer, primary_key=True)
    contype = db.Column(db.String(10))
    conway = db.Column(db.String(20))
    phoneno = db.Column(db.Integer)
    hyperlink = db.Column(db.String)