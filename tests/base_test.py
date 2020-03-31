"""
This module is used as a base for all other test cases.
"""
import unittest

from config import TestingConfig
from project import create_app


class BaseTestCase(unittest.TestCase):
    """
    Inherits unittest.TestCase
    """

    def setUp(self):
        """
        Sets up our Flask App
        :return: void
        """
        self.app = create_app(app_config=TestingConfig)
        self.client = self.app.test_client()

    def tearDown(self):
        """ Not used """
        pass
