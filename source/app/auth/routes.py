from flask import render_template, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app.models import User
from app.auth import bp
from app.auth.forms import LoginForm


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('projects_tab.projects'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        current_app.logger.info(f'user:{current_user.email} role:{current_user.user_role} LOGIN')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('projects_tab.projects')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    current_app.logger.info(f'user:{current_user.email} role:{current_user.user_role} LOGOUT')
    logout_user()
    return redirect(url_for('auth.login'))