"""All routes for university system"""


from typing import Union

from flask import render_template, request, redirect, Response

from . import app
from .business_logic import (
    _get_student_data_from_form,
    _add_new_student,
    _get_available_groups,
    _create_new_group,
    _get_data_about_group,
    _get_students_from_group
)


@app.route('/')
def index() -> str:
    """Main page."""
    return render_template("index.html")


@app.route('/add_new_group', methods=('GET', 'POST'))
def add_new_group() -> Union[str, Response]:
    """Page to create and watch another groups."""
    if request.method == 'POST':
        group_name = request.form.get('group_name')
        _create_new_group(group_name)
        return redirect("add_new_group")
    title = 'Add group'
    return render_template(
        'group_management.html',
        title=title,
        all_groups=[group.group_name for group in _get_available_groups()]
    )


@app.route("/group_list/<group_name>")
def show_table_of_students_in_group(group_name) -> str:
    """Show page with table of students in group."""
    return render_template(
        "group_list.html",
        group_name=_get_data_about_group(group_name).group_name,
        all_students_in_group=_get_students_from_group(group_name),
        enumerate=enumerate
    )


@app.route("/add_student", methods=("GET", "POST"))
def add_student_to_group() -> Union[str, Response]:
    """Render template with form to add new students."""
    if request.method == 'POST':
        _add_new_student(*_get_student_data_from_form(request))
        return redirect("add_student")
    title = "Add student"
    return render_template(
        "add_student.html",
        title=title,
        available_groups_to_join=_get_available_groups()
        )
