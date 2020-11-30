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
        for an expected error.
    """

    """Scenario: Test Post Instafluencer No Account Fail"""
    def test_c_post_instafluencer_by_no_account(self):

        res = self.client().post('/insta-fluencers',
                                 json=self.new_instafluencer,
                                 headers=[
                                     ('Content-Type', 'application/json')
                                 ])
        data = res.json

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """Scenario: Test Post Instafluencer Standard Account Fail"""
    def test_d_post_instafluencer_by_standard_account(self):

        res = self.client().post('/insta-fluencers',
                                 json=self.new_instafluencer,
                                 headers=[
                                     ('Content-Type', 'application/json'),
                                     ('Authorization', self.standard)
                                 ])
        data = res.json

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """Scenario: Test Post Instafluencer Premium Account Success"""
    def test_e_post_instafluencer_by_premium_account(self):

        res = self.client().post('/insta-fluencers',
                                 json=self.new_instafluencer,
                                 headers=[
                                     ('Content-Type', 'application/json'),
                                     ('Authorization', self.premium)
                                 ])
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        """Scenario: Test Post SavedInsta No Account Fail"""
        def test_c_post_savedInst_by_no_account(self):

            res = self.client().post('/saved-insta-fluencers',
                                     json={
                                            "searcher_username":
                                            os.environ['STANDUSER'],
                                            "insta_fluencer_id": 1
                                        },
                                     headers=[
                                         ('Content-Type', 'application/json')
                                     ])
            data = res.json

            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)

        """Scenario: Test Post SavedInsta Standard Account Fail"""
        def test_d_post_savedInsta_by_standard_account(self):

            res = self.client().post('/saved-insta-fluencers',
                                     json={
                                            "searcher_username":
                                            os.environ['STANDUSER'],
                                            "insta_fluencer_id": 1
                                        },
                                     headers=[
                                         ('Content-Type', 'application/json'),
                                         ('Authorization', self.standard)
                                     ])
            data = res.json

            self.assertEqual(res.status_code, 401)
            self.assertEqual(data['success'], False)

        """Scenario: Test Post SavedInsta Premium Account Success"""
        def test_e_post_savedInsta_by_premium_account(self):

            res = self.client().post('/saved-insta-fluencers',
                                     json={
                                            "searcher_username":
                                            os.environ['PREMUSER'],
                                            "insta_fluencer_id": 1
                                        },
                                     headers=[
                                         ('Content-Type', 'application/json'),
                                         ('Authorization', self.premium)
                                     ])
            data = res.json

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)

        """Scenario: Test Get SavedInsta Premium Account Success"""
        def test_e_get_savedInsta_by_premium_account(self):

            res = self.client().get('/saved-insta-fluencers',
                                    headers={"Authorization":
                                             self.premium})
            data = res.json

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)

        """Scenario: Test Get SavedInsta Standard Account Failed"""
        def test_e_get_savedInsta_by_standard_account(self):

            res = self.client().get('/saved-insta-fluencers',
                                    headers={"Authorization":
                                             self.standard})
            data = res.json

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)

        """Scenario: Test Get SavedInsta No Account Failed"""
        def test_e_get_savedInsta_by_no_account(self):

            res = self.client().get('/saved-insta-fluencers')
            data = res.json

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)

        """Scenario: Test Search Instafluencers - Success """
        def test_a_search_instafluencers_by_anyone(self):

            res = self.client().post('/insta-fluencers/search',
                                     json={"search_term": "college radio"},
                                     headers=[
                                         ('Content-Type', 'application/json')
                                     ])
            data = res.json

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)

        """Scenario: Test Search Instafluencers - Fail """
        def test_b_search_instafluencers_by_anyone(self):

            res = self.client().post('/insta-fluencers/search',
                                     json={"searchTerm": "college radio"},
                                     headers=[
                                         ('Content-Type', 'application/json')
                                     ])
            data = res.json

            self.assertEqual(res.status_code, 400)
            self.assertEqual(data['success'], False)

    """Scenario: Test Patch Instafluencer Premium Account Success"""
    def test_f_patch_instafluencer_by_premium_account(self):

        res = self.client().patch('/insta-fluencers/1',
                                  json={"engagement": 15},
                                  headers=[
                                     ('Content-Type', 'application/json'),
                                     ('Authorization', self.premium)
                                     ])
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    """Scenario: Test Patch Instafluencer Premium Account Fail"""
    def test_g_patch_instafluencer_by_premium_account_not_found(self):

        res = self.client().patch('/insta-fluencers/1000',
                                  json={"engagement": 15},
                                  headers=[
                                     ('Content-Type', 'application/json'),
                                     ('Authorization', self.premium)
                                     ])
        data = res.json

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    """Scenario: Test Patch Instafluencer No Account Fail"""
    def test_h_patch_instafluencer_by_no_account_unauthorized(self):

        res = self.client().patch('/insta-fluencers/1',
                                  json={"engagement": 15},
                                  headers=[
                                     ('Content-Type', 'application/json'),
                                     ])
        data = res.json

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """Scenario: Test Delete Instafluencer No Account Fail"""
    def test_i_delete_instafluencer_by_no_account_unauthorized(self):

        res = self.client().delete('/insta-fluencers/1',
                                   headers=[
                                        ('Content-Type', 'application/json'),
                                        ])
        data = res.json

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """Scenario: Test Delete Instafluencer Premium Account Success"""
    def test_j_delete_instafluencer_by_premium_account_success(self):

        res = self.client().delete('/insta-fluencers/1',
                                   headers=[
                                        ('Content-Type', 'application/json'),
                                        ('Authorization', self.premium)
                                        ])
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    """Scenario: Test Delete Instafluencer Premium Account Fail: Not Found"""
    def test_k_delete_instafluencer_by_premium_account_not_found(self):

        res = self.client().delete('/insta-fluencers/1000',
                                   headers=[
                                        ('Content-Type', 'application/json'),
                                        ('Authorization', self.premium)
                                        ])
        data = res.json

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    """Scenario: Test Delete SavedInsta No Account Fail"""
    def test_l_delete_saved_by_no_account_unauthorized(self):

        res = self.client().delete('/saved-insta-fluencers/1',
                                   headers=[
                                        ('Content-Type', 'application/json'),
                                        ])
        data = res.json

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """Scenario: Test Delete SavedInsta Premium Account Success"""
    def test_m_delete_saved_by_premium_account_success(self):

        res = self.client().delete('/saved-insta-fluencers/1',
                                   headers=[
                                        ('Content-Type', 'application/json'),
                                        ('Authorization', self.premium)
                                        ])
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    """Scenario: Test Delete Saved Premium Account Fail: Not Found"""
    def test_n_delete_saved_by_premium_account_not_found(self):

        res = self.client().delete('/saved-insta-fluencers/1000',
                                   headers=[
                                        ('Content-Type', 'application/json'),
                                        ('Authorization', self.premium)
                                        ])
        data = res.json

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    """Scenario: Test Delete SavedInsta Standard Account Success"""
    def test_o_delete_saved_by_standard_account_success(self):

        res = self.client().delete('/saved-insta-fluencers/1',
                                   headers=[
                                        ('Content-Type', 'application/json'),
                                        ('Authorization', self.standard)
                                        ])
        data = res.json

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable

if __name__ == "__main__":
    unittest.main()
