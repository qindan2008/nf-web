# This file defines command line commands for manage.py
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import sys

from nf_web.app import db, create_app


def init_db(db, app):
    """ Initialize the database."""
    db.drop_all(app=app)
    db.create_all(app=app)
    print("Db recreated")


def destroy_db(db, app):
    db.drop_all(app=app)
    print("Db destroyed")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        app = create_app()
        if command == "create":
            init_db(db, app)
        elif command == "destroy":
            destroy_db(db, app)
        else:
            raise ValueError("Unknown command")
    else:
        raise ValueError("No command specified")


    # create_users()

#
# def create_users():
#     """ Create users """
#
#     # Create all tables
#     db.create_all()
#
#     # Adding roles
#     admin_role = find_or_create_role('admin', u'Admin')
#
#     # Add users
#     user = find_or_create_user(u'Admin', u'Example', u'admin@example.com', 'Password1', admin_role)
#     user = find_or_create_user(u'Member', u'Example', u'member@example.com', 'Password1')
#
#     # Save to DB
#     db.session.commit()
#
#
# def find_or_create_role(name, label):
#     """ Find existing role or create new role """
#     role = Role.query.filter(Role.name == name).first()
#     if not role:
#         role = Role(name=name, label=label)
#         db.session.add(role)
#     return role
#
#
# def find_or_create_user(first_name, last_name, email, password, role=None):
#     """ Find existing user or create new user """
#     user = User.query.filter(User.email == email).first()
#     if not user:
#         user = User(email=email,
#                     first_name=first_name,
#                     last_name=last_name,
#                     password=current_app.user_manager.password_manager.hash_password(password),
#                     active=True,
#                     email_confirmed_at=datetime.datetime.utcnow())
#         if role:
#             user.roles.append(role)
#         db.session.add(user)
#     return user
#
#

