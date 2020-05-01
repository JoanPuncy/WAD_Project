from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import current_app, db
from app.main.forms import EditProfileForm, ReportForm, TicketForm
from app.models import User, Cinemas, Reports, Facility, Ticket, Price, Movie, M_Category
from app.main import bp


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title=_('Home'))


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.u_email = form.u_email.data
        current_user.u_phone = form.u_phone.data
        current_user.u_person = form.u_person.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.u_email.data = current_user.u_email
        form.u_phone.data = current_user.u_phone
        form.u_person.data = current_user.u_person
    return render_template('edit_profile.html', title=_('Edit Profile'), form=form)


@bp.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    form = ReportForm(current_user.username)
    if form.validate_on_submit():
        reports = Reports(r_email=form.r_email.data, r_phone=form.r_phone.data,
                          r_category=form.r_category.data, r_title=form.r_title.data, r_body=form.r_body.data,
                          author=current_user)
        db.session.add(reports)
        db.session.commit()
        flash(_('Your enquiry have been submit.'))
        return redirect(url_for('main.user'))
    return render_template('report.html', title=_('Enquiry/Report'), form=form)


@bp.route('/ticket', methods=['GET', 'POST'])
@login_required
def ticket():
    form = TicketForm(current_user.username)
    if form.validate_on_submit():
        tickets = Ticket(c_num=form.c_num.data, m_num=form.m_num.data, p_person=form.p_person.data,
                         p_role=form.p_role.data, t_date=form.t_date.data, p_price=form.p_price.data,
                         t_payment=form.t_payment.data)
        db.session.add(tickets)
        db.session.commit()
        flash(_('Submit Success!'))
        return redirect(url_for('main.user'))
    return render_template('ticket.html', title=_('Ticket'), form=form)


def price():
    form = TicketForm(current_user.username)
    if form.validate_on_submit():
        prices = Price(p_role=form.u_person.data, p_person=form.p_person.data, t_date=form.t_date.data,
                       p_price=form.p_price.data)
        db.session.add(prices)
        db.session.commit()
        return redirect(url_for('main.user'))
    elif request.method == 'GET':
        form.p_role.data = current_user.u_person
    return render_template('ticket.html', title=_('Ticket'), form=form)


@bp.route('/movie_category', methods=['GET', 'POST'])
def movie_category():
    return render_template('movie_category.html', title=_('Movie Category'))


@bp.route('/cinemas', methods=['GET', 'POST'])
def cinemas():
    return render_template('cinemas.html', title=_('Cinemas'))
