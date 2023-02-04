"""All logic for the application here"""


from typing import Iterable, Optional

from flask import Request
from werkzeug.security import generate_password_hash

from . import login_manager
from .database.db_model import session
from .database.student import Student
from .database.group import Group
from .database.user import User
from .forms import SignupLoginForm


def _get_student_data_from_form(request: Request) -> tuple:
    """Get form data about new student."""
    name = request.form.get("name")
    surname = request.form.get("surname")
    age = request.form.get("age")
    address = request.form.get("address")
    group_id = request.form.get("group-id-from-name")
    return name, surname, age, address, group_id


def _add_new_student(
    name: str,
    surname: str,
    age: int,
    address: str,
    group_id: int
) -> None:
    """Add new student to db if all data is not null.
    :param name: a name of new user
    :param surname: a surname of new user
    :param age: an age of new user
    :param address: an address of new user
    :param group_id: add student to group by given group id
    """
    if all((name, surname, age, address, group_id)):
        student = Student(
            surname=surname, name=name,
            age=age, address=address, group=group_id
        )
        session.add(student)
        session.commit()


def _create_new_group(group_name: str) -> None:
    """Create new group and add it to db.
    :param group_name: a group to add new student
    """
    if group_name != "":
        group_to_add = Group(group_name)
        session.add(group_to_add)
        session.commit()


def _get_available_groups() -> Iterable[Group]:
    """Return all available groups for joining and manipulating.
    :return: list of available groups
    """
    return list(group for group in session.query(Group).all())


def _get_data_about_group(group_name: str) -> Optional[Group]:
    """Get group data from db by group name.
    :return: group by the given name if exists else None
    """
    return session.query(Group).where(Group.group_name == group_name).first()


def _get_students_from_group(group_name: str) -> Iterable[Student]:
    """Get students from db by group name.
    :param group_name: add new student to group by the given group name
    """
    return session.query(Student).where(
        Student.group == _get_data_about_group(group_name).id
        ).all()


def _get_data_from_user_form(form: SignupLoginForm) -> tuple:
    """Get data from user login and signup forms."""
    return form.username.data, form.password.data, form.remember_me.data


def _add_new_user(username: str, password: str) -> None:
    """Add new user to the database with secure password hashing."""
    new_user = User(username=username, password=generate_password_hash(password))
    session.add(new_user)
    session.commit()


def _get_existing_user(username: str) -> Optional[User]:
    """Check if there is a user with the given username."""
    user = session.query(User).where(User.username == username).first()
    return user


@login_manager.user_loader
def load_user(user_id) -> Optional[User]:
    """Load user if he exists.
    :param user_id: user's id
    :returns: User or None
    """
    return session.query(User).get(int(user_id))
