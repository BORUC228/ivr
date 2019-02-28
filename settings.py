from unittest import TestCase
from coloredlogs import install
from psycopg2 import connect


class BaseSettings(TestCase):
    db = None


@classmethod
def setUpClass(cls):
    install(level='DEBUG')
    host = '107.16.102.96:5432'
    # here you can edit your base url
    cls.ApiUrl = "http://172.16.102.95:8085"
    # here you can edit your database connection credentials
    cls.db = connect(host=host,
                     user='postgres',
                     password='postgres',
                     database='customer_mgt')


@classmethod
def tearDownClass(cls):
    cls.db.close()
    print("------test is over------")
