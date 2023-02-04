"""All routes for university system"""


from typing import Union

from flask import render_template, request, redirect, url_for, flash, Response
from flask_login import login_required, logout_user, login_user
from werkzeug.security import check_password_hash

from . import app
from .business_logic import (
    _get_student_data_from_form,
    _add_new_student,
    _get_available_groups,
    _create_new_group,
    _get_data_about_group,
    _get_students_from_group,
    _add_new_user,
    _get_existing_user,
    _get_data_from_user_form
)
from .forms import SignupLoginForm


@app.get('/')
def index() -> str:
    """Main page."""
    return render_template("index.html")


@app.get('/add_new_group')
def add_new_group_get() -> Union[str, Response]:
    """Page to create and watch another groups."""
    title = 'Add group'
    return render_template(
        'group_management.html',
        title=title,
        all_groups=[group.group_name for group in _get_available_groups()]
    )


@app.post('/add_new_group')
@login_required
def add_new_group() -> Union[str, Response]:
    """Page to create and watch another groups."""
    group_name = request.form.get('group_name')
    _create_new_group(group_name)
    return redirect("add_new_group")


@app.get("/group_list/<group_name>")
def show_table_of_students_in_group(group_name: str) -> str:
    """Show page with table of students in group.
    :param group_name: name of group to specify from where to take students
    """
    return render_template(
        "group_list.html",
        group_name=_get_data_about_group(group_name).group_name,
        all_students_in_group=_get_students_from_group(group_name),
        enumerate=enumerate
    )


@app.get("/add_student")
def add_student_to_group_get() -> Union[str, Response]:
    """Render template with form to add new students."""
    title = "Add student"
    return render_template(
        "add_student.html",
        title=title,
        available_groups_to_join=_get_available_groups()
    )


@app.post("/add_student")
@login_required
def add_student_to_group() -> Union[str, Response]:
    """Render template with form to add new students."""
    _add_new_student(*_get_student_data_from_form(request))
    return redirect("add_student")


@app.route('/signup', methods=("GET", "POST"))
def signup() -> Union[str, Response]:
    """Sign up new user to the university system."""
    form = SignupLoginForm()
    if request.method == 'POST':
        username, password = _get_data_from_user_form(form)[:2]
        if _get_existing_user(username):
            flash(message="This user already exists.")
            return redirect("signup")
        _add_new_user(username, password)
        return redirect("login")
    return render_template("signup.html", form=form)


@app.route("/login", methods=("GET", "POST"))
def login() -> Union[str, Response]:
    """Log In existing user to the university system."""
    form = SignupLoginForm()
    if form.validate_on_submit():
        username, password, remember_me = _get_data_from_user_form(form)
        user = _get_existing_user(username)
        if not user or not check_password_hash(user.password, password):
            flash("Wrong username or password")
            return redirect(url_for("login"))
        login_user(user, remember=bool(remember_me))
        return redirect(url_for("index"))
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
