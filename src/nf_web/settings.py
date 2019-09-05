# Settings common to all environments (development|staging|production)
# Place environment specific settings in env_settings.py
# An example file (env_settings_example.py) can be used as a starting point

import os

# Application settings
APP_NAME = "NF-web"
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

# Flask settings
CSRF_ENABLED = True

# Flask-User settings
USER_APP_NAME = APP_NAME
USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
USER_ENABLE_CHANGE_USERNAME = False  # Allow users to change their username
USER_ENABLE_CONFIRM_EMAIL = True  # Force users to confirm their email
USER_ENABLE_FORGOT_PASSWORD = True  # Allow users to reset their passwords
USER_ENABLE_EMAIL = True  # Register with Email
USER_ENABLE_REGISTRATION = True  # Allow new users to register
USER_REQUIRE_RETYPE_PASSWORD = True  # Prompt for `retype password` in:
USER_ENABLE_USERNAME = False  # Register and Login with username
USER_AFTER_LOGIN_ENDPOINT = 'main.status'
USER_AFTER_LOGOUT_ENDPOINT = 'main.status'
USER_LOGIN_TEMPLATE = 'flask_user/login_or_register.html'
USER_REGISTER_TEMPLATE = 'flask_user/login_or_register.html'

# DO NOT use "DEBUG = True" in production environments
DEBUG = True

# DO NOT use Unsecure Secrets in production environments
# Generate a safe one with:
#     python -c "import os; print repr(os.urandom(24));"
SECRET_KEY = 'This is an UNSECURE Secret. CHANGE THIS for production environments.'

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///../app.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids a SQLAlchemy Warning

# Flask-Mail settings
# For smtp.gmail.com to work, you MUST set "Allow less secure apps" to ON in Google Accounts.
# Change it in https://myaccount.google.com/security#connectedapps (near the bottom).
MAIL_SERVER = 'mail.sanger.ac.uk'
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_USERNAME = 'cellgeni-su@sanger.ac.uk'
MAIL_PASSWORD = "Bainu'z3"

# MAIL_SERVER = 'smtp.ukr.net'
# MAIL_PORT = 2525
# MAIL_USE_SSL = True
# MAIL_USE_TLS = False
# MAIL_USERNAME = 'anton.khodak@ukr.net'
# MAIL_PASSWORD = 'tschertschesov'
MAIL_DEFAULT_SENDER = f'"NF-web" <{MAIL_USERNAME}>'

# Flask-User settings
USER_EMAIL_SENDER_NAME = "Cellgeni Team"
USER_EMAIL_SENDER_EMAIL = f"{MAIL_USERNAME}"

# Sendgrid settings
SENDGRID_API_KEY='place-your-sendgrid-api-key-here'


ADMINS = [
    '"Admin One" <cellgeni-su@sanger.ac.uk>',
    ]

UPLOAD_FOLDER = '/tmp'