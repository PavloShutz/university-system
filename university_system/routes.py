from flask import render_template, request, redirect

from . import app
from .database.db_model import session
from .database.group import Groups
from .database.student import Student


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/group', methods=('GET', 'POST'))
def group():
    all_data = session.query(Groups).all()
    all_data = [i.group_name for i in all_data]
    if request.method == 'POST':
        group_name = request.form.get('group_name')
        if group_name != "":
            group_to_add = Groups(group_name)
            session.add(group_to_add)
            session.commit()
            return redirect("group")
    title = 'Add group'
    return render_template('group_management.html', title=title, all_groups=all_data)


@app.route("/group_list/<g_name>")
def group_list(g_name):
    gr_id = session.query(Groups).where(Groups.group_name == g_name).first().id
    group_name = session.query(Groups).where(Groups.group_name == g_name).first().group_name
    students_in_group = session.query(Student).where(Student.group == gr_id).all()
    return render_template("group_list.html", group_name=group_name, group=students_in_group, enumerate=enumerate)


def _get_student_data() -> tuple:
    name = request.form.get("name")
    surname = request.form.get("surname")
    age = request.form.get("age")
    address = request.form.get("address")
    group_id = request.form.get("group-id-from-name")
    return name, surname, age, address, group_id


@app.route("/add_student", methods=("GET", "POST"))
def add_student():
    if request.method == 'POST':
        name, surname, age, address, group_id = _get_student_data()
        if all((name, surname, age, address, group_id)):
            student = Student(
                surname=surname, name=name,
                age=age, address=address, group=group_id
            )
            session.add(student)
            session.commit()
        return redirect("add_student")
    title = "Add student"
    available_groups = [gr for gr in session.query(Groups).all()]
    return render_template("add_student.html", title=title, available_groups=available_groups)
