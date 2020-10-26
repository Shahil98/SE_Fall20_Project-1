from django.db import models
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.core import serializers
import uuid
import json
from django.db.utils import IntegrityError

# Create your models here.
'''
    ---models.py---
    Structure
    Models: User, TimeLog
    Managers: UserManager, TimeLogManager
'''


class UserManager(models.Manager):
    '''

    APIs for the User
    Performs User actions (CRUD operations)
    for signup, login and updating user.

    '''

    def get_user_from_username(self, username, password):
        """
        Returns the user details using the login credentails (basic auth) of the user.

        :param str username: username of the user
        :param str password: password of user
        :return: dictionary response
        :rtype: object
        """
        user = self.filter(username=username, password=password).first()
        if user:
            return {
                "username": user.username,
                "password": user.password,
                "api_token": user.api_token,
            }
        return None

    def get_user_from_api_token(self, api_token):
        """
        Returns the user details using the unique API token of the user.

        :param str api_token: unique apitoken of user
        :return: dictionary response
        :rtype: object
        """
        user = self.filter(api_token=api_token).first()
        if user:
            return {
                "username": user.username,
                "password": user.password,
                "api_token": user.api_token,
            }
        return None

    @staticmethod
    def create_user(user):
        """
        Create a new user.

        :param dict user: validated user details from post request
        :return: response status (0 for failure, 1 for success and 2 for DB error)
        :rtype: int
        """
        user["api_token"] = str(uuid.uuid4()) + get_random_string(length=16)

        user_instance = User(**user)
        try:
            if not user_instance.save():
                return 0
            return 1
        except IntegrityError as e:
            print(e)
            return 2

    def update_user(self, user, api_token):
        """
        Update user information.

        :param dict user: validated user details from post request
        :param str api_token: unique apitoken of user
        :return: response status (0 for success, 1 for no such user with api_token)
        :rtype: int
        """
        user_instance = self.filter(api_token=api_token)

        if user_instance:
            user_instance.update(**user)
            return 0
        return 1

    def login(self, username, password):
        """
        Login a user using basic auth

        :param str username: username of the user
        :param str password: password of user
        :return: api_token is such user exists
        :rtype: str
        """
        user_info = self.filter(username=username, password=password).first()

        if user_info:
            return user_info["api_token"]
        return -1


class User(models.Model):
    '''
    Description for User DB Model

    :ivar log_user_id: Primary key indexing each user
    :ivar username: unique username of the user
    :ivar password: password of the user
    :ivar api_token: unique token for each user stored for sublime activity
    '''

    class Meta:
        db_table = "log_user"

    log_user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, blank=False, null=False, max_length=100)
    password = models.CharField(blank=False, null=False, max_length=100)
    api_token = models.CharField(max_length=200)
    objects = UserManager()


class TimeLogManager(models.Manager):
    @staticmethod
    def create_log(time_log):
        """
        Create a new log for a file for a particular user

        :param dict time_log: validated time log details from post request
        :return: return status
        :rtype: int
        """
        time_log_instance = TimeLog(**time_log)

        try:

            if not time_log_instance.save():
                return 0
            return 1
        except Exception:
            return 1

    def create_time_log(
        self, api_token, file_name, file_extension, detected_language, log_date, log_timestamp
    ):
        """
        Create a new log for a file for a particular user

        :param str api_token: unique token for each user
        :param str file_name: file being edited by user
        :param str file_extension: extension of the file (or file type)
        :param str detected_language: language in the file
        :param str log_date: date of when was the file logged
        :param str log_timestamp: time recorded for activity on file
        :return: api_token on success
        :rtype: str
        """
        try:
            user = User.objects.filter(api_token=api_token).first()
            file_log = self.filter(log_user_id=user, file_name=file_name).first()
            if file_log is not None:
                log_timestamp = file_log.log_timestamp + log_timestamp
                self.filter(log_user_id=user, file_name=file_name).update(
                    log_timestamp=log_timestamp, modified_at=now()
                )
            else:
                self.create(
                    log_user_id=user,
                    file_name=file_name,
                    file_extension=file_extension,
                    detected_language=detected_language,
                    log_date=log_date,
                    log_timestamp=log_timestamp,
                )

            return api_token
        except Exception as e:
            print("error in creating logs for user ", e)
            return e

    def get_time_logs(self, api_token):
        """
        Get all the filelogs for a particular user

        :param str api_token: unique token for each user
        :return: list of all the file logs of the user
        :rtype: list
        """
        try:
            logs = self.filter(api_token=api_token).all()
            return json.loads(serializers.serialize("json", [log for log in logs]))
        except Exception as e:
            print("error in getting logs for user ", e)
            return e


class TimeLog(models.Model):
    '''
    Description for Time Logging DB Model

    :ivar log_file_time_id: Primary key indexing each time log of a file of a user
    :ivar api_token: unique token for each user
    :ivar file_name: file being edited by user
    :ivar file_extension: extension of the file (or file type)
    :ivar detected_language: language in the file
    :ivar log_date: date of when was the file logged
    :ivar log_timestamp: time recorded for activity on file
    :ivar created_at: timestamp of when file was created
    :ivar modified_at: timestamp of when file was modified last
    '''

    class Meta:
        db_table = "log_file_time"

    log_file_time_id = models.AutoField(primary_key=True)
    api_token = models.CharField(max_length=200, null=False, blank=False)
    file_name = models.CharField(max_length=1000, null=False, blank=False)
    file_extension = models.CharField(max_length=20, null=True, blank=True)
    detected_language = models.CharField(max_length=50, null=True, blank=True)
    log_date = models.DateField(blank=False, null=False)
    log_timestamp = models.FloatField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    objects = TimeLogManager()
