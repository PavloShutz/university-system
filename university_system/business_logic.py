from typing import Iterable

from flask import Request

from .database.db_model import session
from .database.student import Student
from .database.group import Group


def _get_student_data_from_form(request: Request) -> tuple:
    """Get form data about new student."""
    name = request.form.get("name")
    surname = request.form.get("surname")
    age = request.form.get("age")
    address = request.form.get("address")
    group_id = request.form.get("group-id-from-name")
    return name, surname, age, address, group_id


def _add_new_student(name: str, surname: str, age: int, address: str, group_id: int):
    """Add new student to db if all data is not null."""
    if all((name, surname, age, address, group_id)):
        student = Student(
            surname=surname, name=name,
            age=age, address=address, group=group_id
        )
        session.add(student)
        session.commit()


def _create_new_group(group_name: str) -> None:
    """Create new group and add it to db."""
    if group_name != "":
        group_to_add = Group(group_name)
        session.add(group_to_add)
        session.commit()


def _get_available_groups() -> Iterable[list[Group]]:
    """Return all available groups for joining and manipulating."""
    return [group for group in session.query(Group).all()]


def _get_data_about_group(group_name: str):
    """Get group data from db by group name."""
    return session.query(Group).where(Group.group_name == group_name).first()


def _get_students_from_group(group_name: str):
    """Get students from db by group name."""
    return session.query(Student).where(Student.group == _get_data_about_group(group_name).id).all()
