
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import unittest
 
from run import app

from flask import session

class TestSprint4(unittest.TestCase):
    #Test 'search' route for existing visittoPlace entry
    def test_search_with_session(self):
        tester = app.test_client(self)

        with tester.session_transaction() as session:
            session['current_user_type'] = 'Agent'
            session['current_user'] = 'Agent'

        response = tester.post('/search', data=dict(visitor_name="admin", entry="2022-04-01T15:11", exit="2022-05-06T15:11"), follow_redirects=True)
        self.assertIn(b'<table class = "table">', response.data)
 
    #Test 'search' route for non-existing visittoPlace entry
    def test_search_with_session_false(self):
        tester = app.test_client(self)

        with tester.session_transaction() as session:
            session['current_user_type'] = 'Agent'
            session['current_user'] = 'Agent'

        response = tester.post('/search', data=dict(visitor_name="user1", entry="2022-05-01T15:11", exit="2022-05-06T15:11")
        , follow_redirects=True)
        self.assertIn(b'did not visit any places between ', response.data)

    #Test 'searchv' route for existing visittoPlace entry
    def test_searchv_with_session(self):
        tester = app.test_client(self)

        with tester.session_transaction() as session:
            session['current_user_type'] = 'Agent'
            session['current_user'] = 'Agent'

        response = tester.post('/searchv', data=dict(place_name="admin", entry="2022-04-01T15:11", exit="2022-05-06T15:11")
        , follow_redirects=True)

        self.assertIn(b'<table class = "table">', response.data)
 
    #Test 'searchv' route for non-existing visittoPlace entry
    def test_searchv_with_session_false(self):
        tester = app.test_client(self)

        with tester.session_transaction() as session:
            session['current_user_type'] = 'Agent'
            session['current_user'] = 'Agent'

        response = tester.post('/searchv', data=dict(place_name="place1", entry="2022-05-01T15:11", exit="2022-05-06T15:11")
        , follow_redirects=True)

        self.assertIn(b"There weren't any visitors to place1", response.data)


if __name__ == '__main__':
    unittest.main()