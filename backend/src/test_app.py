import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

from flaskr import create_app
from models import setup_db, Instafluencer, SavedInsta

"""
    REST API Testing Strategy Link:
        https://www.sisense.com/blog/
            rest-api-testing-strategy-what-exactly-should-you-test/
    Example: txt3 = "My name is {}, I'am {}".format("John",36)
"""


class InstafluencerTestCase(unittest.TestCase):
    """This class represents the instafluencer test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.standard = os.environ['STANDARD']
        self.premium = os.environ['PREMIUM']
        self.database_name = os.environ['TEST_DATABASE_NAME']
        self.database_path = "postgres://{}/{}". \
            format(os.environ['TEST_PORT'], self.database_name)

        # connect test app to test db
        setup_db(self.app, self.database_path)

        # define any objects to be used in tests
        self.new_instafluencer = {
            "username": "anjee_smiles",
            "full_name": "Anjenée",
            "profile_pic_link": "https://scontent-atl3-2.cdninstagram.com/\
                v/t51.2885-19/s150x150/45466966_323990854861643_\
                3648830650758201344_n.jpg?_nc_ht=scontent-atl3-2.cdninstagram.\
                com&_nc_ohc=6uwDtqxJfVwAX-7yU_R&oh=\
                cd1bfb665b6331a0e3c193750ca7b3ec&oe=5FCAE768",
            "profile_link": "https://www.instagram.com/anjee_smiles/",
            "followers": 3100,
            "posts_per_week": 0.5,
            "enagement": 19.1,
            "hashtags": ["college radio", "radio host"]
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    """
        Write at least one test for each test for successful operation and
        for expected errors.
    """

    """Scenario: Test Get Categories """
    def test_get_categories(self):

        res = self.client().get('/categories')

        # returns a list with string keys
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        #these values may vary so just make sure they
        #exist by checking if the return True
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    """Scenario: Test 405 Sent When POST to Categories"""
    def test_405_post_to_categories(self):

        res = self.client().post('/categories', json=self.new_question)

        #returns a list with string keys
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

        #check error message
        self.assertEqual(data['message'],'method not allowed')


    """Scenario: Test 200 Sent When POST New Questions"""
    def test_200_post_new_question(self):

        res = self.client().post('/questions', json=self.new_question)

        #returns a list with string keys
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    """Scenario: Test 400 Sent When Incomplete POST to Add Question"""
    def test_400_incompelete_question_add(self):

        bad_request_question = {
        'answer': "I hope so",
        'category': "Entertainment",
        'difficulty': 2
        }

        res = self.client().post('/questions', json=bad_request_question)

        #returns a list with string keys
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

        #check error message
        self.assertEqual(data['message'],'bad request')

    """Scenario: Test SearchTerm Questions """
    def test_searchterm_questions(self):

        searchTerm = {'searchTerm': 'title'}

        res = self.client().post('/questions', json = searchTerm)

        #returns a list with string keys
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        #these values may vary so just make sure they
        #exist by checking if the return True
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

        #search and confirm hope is in each result string
        matches = [match for match in data['questions'] if "title" in match['question']]

        self.assertEqual(len(data['questions']),len(matches))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])


    """Scenario: Test Delete Question"""
    def test_200_delete_question(self):

        res = self.client().delete('/questions/15')

        #returns a list with string keys
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 15).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None)

    """Scenario: Test Delete Question Not There"""
    def test_422_delete_question_not_there(self):

        res = self.client().delete('/questions/1000')

        #returns a list with string keys
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

        #check error message
        self.assertEqual(data['message'],'unprocessable')

    """Test Get Paginated Questions """
    def test_get_paginated_questions(self):

        res = self.client().get('/questions?page=2')

        #returns a list with string keys
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        #these values may vary so just make sure they
        #exist by checking if the return True
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    """Scenario: Test 404 Sent When Requesting Beyond Valid Page"""
    def test_404_sent_requesting_beyond_valid_page(self):

        res = self.client().get('/questions?page=1000')

        #returns a list with string keys
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

        #check error message
        self.assertEqual(data['message'],'resource not found')


    """Test Get Questions for Specific Category"""
    def test_get_specific_category_questions(self):

        res = self.client().get('/categories/2/questions')

        #returns a list with string keys
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        #these values may vary so just make sure they
        #exist by checking if the return True
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertEqual(data['current_category'], 2)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    """Scenario: Test 404 If Category Id Does Not Exist"""
    def test_404_if_category_does_not_exist(self):

        res = self.client().get('/categories/1000/questions')

        #returns a list with string keys
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

        #check error message
        self.assertEqual(data['message'],'resource not found')


    """Scenario Test 405 Get Quizzes When not allowed """
    def test_405_get_quizzes(self):

        res = self.client().get('/quizzes')

        #returns a list with string keys
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

        #check error message
        self.assertEqual(data['message'],'method not allowed')



    """Scenario: Test 200 Sent When POST to Quizzes"""
    def test_200_post_to_quizzes(self):


        quiz_send = {
        'quiz_category': {'type': 'Geography', 'id': '3'},
        'previous_questions': [self.new_question]
        }

        res = self.client().post('/quizzes', json=quiz_send)

        #returns a list with string keys
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # these values may vary so just make sure they
        # exist by checking if the return True
        self.assertTrue(data['question'])


# Make the tests conveniently executable

if __name__ == "__main__":
    unittest.main()
