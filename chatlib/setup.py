import os
from setuptools import setup
import sys

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Versioning is #0.MAJOR.MINOR.PATCH


setup(
    name='Chatroom Library',
    version='0.0.1',
    description='Shared functions for the chat room',
    packages=[
        'chatroom',
        'chatroom.db',
    ],
    install_requires=[
        "alembic==1.0.5",
        "psycopg2-binary==2.7.6.1",
        "Flask==1.0.2",
        "SQLAlchemy==1.2.15",

        "Click==7.0",
        "itsdangerous==1.1.0",
        "Jinja2==2.10",
        "Mako==1.0.7",
        "MarkupSafe==1.1.0",
        "python-dateutil==2.7.5",
        "python-editor==1.0.3",
        "six==1.12.0",
        "Werkzeug==0.14.1",
    ],
    dependency_links=[],
    include_package_data=True,
)
