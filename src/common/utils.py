from passlib.hash import pbkdf2_sha512
import re
import hashlib


class Utils(object):

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile(r'^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512->pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the password the user sent matches that of the database.
        The database password is encrypted more that the user's password at this stage.
        :param password: password
        :param hashed_password: sha512 encrypted password
        :return: True if passwords match, False otherwise
        """

        return hashlib.sha512(password.encode('utf-8')).hexdigest() == hashed_password
