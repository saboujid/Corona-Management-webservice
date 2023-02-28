import os, sys
import string
import random
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import tempfile
import unittest
 
from run import app


class TestBase(unittest.TestCase):

    # The login is successful for correct credentials
    def test_agent_login_successful(self):
        tester = app.test_client(self)
        response = tester.post('/login_agent', data=dict(username="Agent", password="12345"), follow_redirects=True)
        self.assertIn(b'Register', response.data)

    # The login is not successful for incorrect credentials
    def test_agent_login_unsuccessful(self):
        tester = app.test_client(self)
        response = tester.post('/login_agent_page', data=dict(username="wrong1", password="wrong"), follow_redirects=True)
        self.assertIn(b'not allowed', response.data)
    
    # The login is successful for correct credentials
    def test_place_login_successful(self):
        tester = app.test_client(self)
        response = tester.post('/login_place', data=dict(username="admin", password="admin"), follow_redirects=True)
        self.assertIn(b'Register', response.data)

    # The login is not successful for incorrect credentials
    def test_place_login_unsuccessful(self):
        tester = app.test_client(self)
        response = tester.post('/login_place_page', data=dict(username="wrong1", password="wrong"), follow_redirects=True)
        self.assertIn(b'not allowed', response.data)

    # User register opens successfully
    def test_place_register_page(self):
        tester = app.test_client(self)
        response = tester.get('/register_place_page', content_type="html/text")
        self.assertIn(b'Login', response.data)

    # The login is successful for correct credentials
    def test_hospital_login_successful(self):
        tester = app.test_client(self)
        response = tester.post('/login_hospital', data=dict(username="admin", password="admin"), follow_redirects=True)
        self.assertIn(b'Register', response.data)

    # The login is not successful for incorrect credentials
    def test_hospital_login_unsuccessful(self):
        tester = app.test_client(self)
        response = tester.post('/login_hospital_page', data=dict(username="wrong1", password="wrong"), follow_redirects=True)
        self.assertIn(b'not allowed', response.data)

    # Instructor register opens successfully
    def test_hospital_register_page(self):
        tester = app.test_client(self)
        response = tester.get('/register_hospital_page', content_type="html/text")
        self.assertIn(b'Login', response.data)

    # The login is successful for correct credentials
    def test_visitor_login_successful(self):
        tester = app.test_client(self)
        response = tester.post('/login_visitor', data=dict(username="admin", password="admin"), follow_redirects=True)
        self.assertIn(b'Register', response.data)

    # The login is not successful for incorrect credentials
    def test_visitor_login_unsuccessful(self):
        tester = app.test_client(self)
        response = tester.post('/login_visitor_page', data=dict(username="wrong1", password="wrong"), follow_redirects=True)
        self.assertIn(b'not allowed', response.data)


    # User register opens successfully
    def test_visitor_register_page(self):
        tester = app.test_client(self)
        response = tester.get('/register_visitor_page', content_type="html/text")
        self.assertIn(b'Login', response.data)

    def test_aboutus_page(self):
        tester = app.test_client(self)
        response = tester.get('/about_us', content_type="html/text")
        self.assertIn(b'about_us', response.data)




if __name__=='__main__':
   unittest.main()