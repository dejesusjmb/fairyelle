import os
import uuid

from src.common.utils import Utils
import src.models.admin.errors as AdminErrors


class Admin(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return '<Admin {}>'.format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an email/password combo (as sent by the site forms) is valid or not.
        :param email: The admin's email
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """

        pw = os.environ.get('ADMIN_PASSWORD')
        if email != os.environ.get('ADMIN_EMAIL'):
            raise AdminErrors.InvalidEmailError('Invalid email')
        if not Utils.check_hashed_password(password, pw):
            raise AdminErrors.IncorrectPasswordError('Incorrect password')

        return True
