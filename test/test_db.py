import pytest
from app.db import *


def test_init_db():
    init_db()


def test_add_user():
    assert add_user('teacher', '123456', 1, 'no_reply@artorius.net') == 1
    assert add_user('student1', 'abcd', 0, 'no_reply@artorius.net') == 2
    assert add_user('student2', 'abcd', 0, 'no_reply@artorius.net') == 3
    assert add_user('bad password', 12345, 1, 'no_reply@artorius.net') == False
    assert add_user(12345, 'bad name', 1, 'no_reply@artorius.net') == False
    assert add_user('bad identity', '123456', 2, 'no_reply@artorius.net') == False


def test_check_password():
    assert check_password(1, '123456') == True
    assert check_password(1, 'abcd') == False
    assert check_password(2, 'abcd') == True
    assert check_password(4, 'no such user') == False
    assert check_password(1, 123456) == False
    assert check_password('1', '123456') == True


def test_get_identity():
    assert get_identity(1) == 1
    assert get_identity(2) == 0
    assert get_identity(3) == 0
    assert get_identity(4) == -1
    assert get_identity('bad id') == -1


def test_check_info():
    assert get_user_info(1) == (1, 'teacher', 1, 'no_reply@artorius.net')
    assert get_user_info(2) == (2, 'student1', 0, 'no_reply@artorius.net')
    assert get_user_info(3) == (3, 'student2', 0, 'no_reply@artorius.net')
    assert get_user_info(4) == None


def test_add_room():
    assert add_room(1, '综合项目实践', '2020年秋学期') == 1
    assert add_room('bad id', 'foo', 'bar') == False
    assert add_room(4, 'foo', 'bar') == False


def test_add_stu():
    assert add_stu(2, 1) == True
    assert add_stu(1, 1) == True
    assert add_stu(3, 1) == True
    assert add_stu(4, 1) == False


def test_get_user_room():
    assert get_user_room(2) == [(1,)]

def test_get_room_info():
    # rooms.id, users.id, username, name, profile
    assert get_room_info(1) == (1, 1, 'teacher', '综合项目实践', '2020年秋学期')

def test_change_user():
    uid = 1
    _, uname, uidentity, address = get_user_info(uid)
    assert change_user(uid, uname, 'qwer', uidentity, address) == True
    assert change_user(uid, uname, '123456', uidentity, address) == True
