import os
from sqlalchemy import exc
import base64
import json
from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from models import db_drop_and_create_all, setup_db, Instafluencer, SavedInsta
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
        Uncomment the following line to initialize the datbase
        !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
        !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''
    # db_drop_and_create_all()

    # ROUTES

    '''
        POST /insta-fluencers/search
            it searches instafluencer table by hashtag
            it should not require any permission to use
        returns status code 200 and json
        {
            'success': True,
            'fluencers': selection,
            'total_fluencers': len(selection),
            'search_term': search_term
        }
    '''

    @app.route('/insta-fluencers/search', methods=['POST'])
    def search_insta_fluencers():

        # get request from the client
        body = request.get_json()

        # get info from the body and if nothing there set it to None
        search_term = body.get('search_term', None)

        print(search_term)

        # pass to helper function
        search_results = search_social(search_term)

        return search_results.data

    '''
        Helper function that takes in a search term and returns a list
        of influencers, total number in the list, the search_term, and success
        code
    '''
    def search_social(search_term):

        try:

            # query Insta db for search_term and arrange by highest engagement
            selection = Instafluencer.query.filter(
                Instafluencer.hashtags.
                ilike('%{}%'.format(search_term))). \
                order_by(Instafluencer.engagement.desc())

            '''
                {} are placeholders for python format() in strings.
                Using {} as placeholders lets you insert all arguments in the
                following () w/o having to worry about indexes numbering or
                naming it auto fills each placeholder in the order the args
                appear
            '''

            if(len(selection) != 0):

                return jsonify({
                    'success': True,
                    'fluencers': selection,
                    'total_fluencers': len(selection),
                    'search_term': search_term
                })

            else:

                abort(404)

        except BaseException:
            abort(404)

    '''
        PATCH /insta-fluencers/<insta_id>
            where <insta_id> is the existing insta_fluencer_id
            it should respond with a 404 error if <insta_id> is not found
            it should update the corresponding row for <insta_id>
            it should require the 'update:influencer' permission
        returns status code 200 and json
        {"success": True, "instafluencer": instafluencer}
        where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
    '''

    @app.route('/insta-fluencers/<int:insta_id>', methods=['PATCH'])
    @requires_auth('update:influencer')
    def update_influencer(jwt, insta_id):
        try:
            instafluencer = Instafluencer.query. \
                filter(Instafluencer.id == insta_id).one_or_none()

            # check if drink even exists
            if instafluencer is None:
                abort(404)

            # get payload for update
            body = request.get_json()

            # see what's being updated and change value
            if "username" in body:
                # get info from the body and if nothing there set it to None
                new_username = body.get('username', None)
                instafluencer.username = new_username

            if "full_name" in body:
                new_full_name = body.get('full_name', None)
                instafluencer.full_name = new_full_name

            if "profile_pic_link" in body:
                new_profile_pic_link = body.get('profile_pic_link', None)
                instafluencer.profile_pic_link = new_profile_pic_link

            if "profile_link" in body:
                new_profile_link = body.get('profile_link', None)
                instafluencer.profile_link = new_profile_link

            if "followers" in body:
                new_followers = body.get('followers', None)
                instafluencer.followers = new_followers

            if "posts_per_week" in body:
                new_posts_per_week = body.get('posts_per_week', None)
                instafluencer.posts_per_week = new_posts_per_week

            if "engagement" in body:
                new_engagement = body.get('engagement', None)
                instafluencer.engagement = new_engagement

            if "hashtags" in body:
                new_hashtags = body.get('hashtags', None)

                # append new hashtag to list
                instafluencer.hashtags.append(new_hashtags)

            instafluencer.update()

            return jsonify({
                "success": True,
                "instafluencer": instafluencer
            })

        except BaseException:
            abort(404)

    '''
        GET /saved
            it should respond with a 404 error if <insta_id> is not found
            it should update the corresponding row for <insta_id>
            it should require the 'update:influencer' permission
        returns status code 200 and json
        {"success": True, "instafluencer": instafluencer}
        where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
    '''

    @app.route('/saved-insta-fluencers')
    @requires_auth('view:saved')
    def get_saved(jwt):
        try:

            # check for here if get_saved messes up. make sure jwt is correct
            string2 = jwt
            print("JWT: ")
            print(jwt)
            decoded_base64 = base64.b64decode(str(string2).split(".")[1]+"==")
            user_name = json.loads(decoded_base64.decode("UTF-8"))['sub']

            print("Username")
            print(user_name)

            saved_list = SavedInsta.query. \
                filter(SavedInsta.searcher_username == user_name). \
                order_by('id').all()

            return jsonify({
                'success': True,
                'saved_list': saved_list
            })

        except BaseException:
            abort(404)

    '''
        POST /insta-fluencers
            it should create a new row in the instafluencer table
            it should require the 'add:influencer' permission
        returns status code 200 and json
        {"success": True, "id": instafluencer.id}
        where instafluencer.id is the id of the newly added instafluencer
            or appropriate status code indicating reason for failure
    '''

    @app.route('/insta-fluencers', methods=['POST'])
    @requires_auth('add:influencer')
    def post_instafluencer(jwt):
        # get request from the client
        body = request.get_json()

        # get info from the body and if nothing there set it to None
        new_username = body.get('username', None)
        new_full_name = body.get('full_name', None)
        new_profile_pic_link = body.get('profile_pic_link', None)
        new_profile_link = body.get('profile_link', None)
        new_followers = body.get('followers', None)
        new_posts_per_week = body.get('posts_per_week', None)
        new_engagement = body.get('engagement', None)
        new_hashtags = body.get('hashtags', None)

        # validate that hashtags are already in a list
        print(new_hashtags)

        try:

            instafluencer = Instafluencer(
                username=new_username,
                full_name=new_full_name,
                profile_pic_link=new_profile_pic_link,
                profile_link=new_profile_link,
                followers=new_followers,
                posts_per_week=new_posts_per_week,
                engagement=new_engagement,
                hashtags=new_hashtags)

            instafluencer.insert()

            return jsonify({
                "success": True,
                "id": instafluencer.id
            })

        except BaseException:
            abort(400)

    '''
        POST /saved-insta-fluencers
            it should create a new row in the savedInsta table
            it should require the 'save:influencer' permission
        returns status code 200 and json
        {"success": True, "id": saved_insta.id}
        where saved.id is the id of the newly added savedInsta entry
            or appropriate status code indicating reason for failure
    '''

    @app.route('/saved-insta-fluencers', methods=['POST'])
    @requires_auth('save:influencer')
    def post_saved(jwt):
        # get request from the client
        body = request.get_json()

        # get info from the body and if nothing there set it to None
        new_username = body.get('searcher_username', None)
        new_insta_fluencer_id = body.get('insta_fluencer_id', None)

        try:

            saved_insta = SavedInsta(
                searcher_username=new_username,
                insta_fluencer_id=new_insta_fluencer_id)

            saved_insta.insert()

            return jsonify({
                "success": True,
                "id": saved_insta.id
            })

        except BaseException:
            abort(400)

    '''
        DELETE /saved-insta-fluencers/<saved_id>
            where <saved_id> is the existing saved model id
            it should respond with a 404 error if <saved_id> is not found
            it should delete the corresponding row for <saved_id>
            it should require the 'unsave:influencer' permission
        returns status code 200 and json {"success": True, "delete": saved_id}
        where saved_id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''

    @app.route('/saved-insta-fluencers/<int:saved_id>', methods=['DELETE'])
    @requires_auth('unsave:influencer')
    def delete_saved(jwt, saved_id):
        try:
            savedInsta = SavedInsta.query. \
                filter(SavedInsta.id == saved_id).one_or_none()

            if savedInsta is None:
                abort(404)

            # delete question from db
            savedInsta.delete()

            return jsonify({
                "success": True,
                "delete": saved_id
            })

        except BaseException:

            abort(404)

    '''
        DELETE /insta-fluencers/<insta_id>
            where <insta_id> is the existing instafluencer model id
            it should respond with a 404 error if <insta_id> is not found
            it should delete the corresponding row for <insta_id>
            it should require the 'delete:influencer' permission
        returns status code 200 and json {"success": True, "delete": insta_id}
        where insta_id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''

    @app.route('/insta-fluencers/<int:insta_id>', methods=['DELETE'])
    @requires_auth('delete:influencer')
    def delete_instafluencer(jwt, insta_id):
        try:
            instafluencer = Instafluencer.query. \
                filter(Instafluencer.id == insta_id).one_or_none()

            if instafluencer is None:
                abort(404)

            # delete question from db
            instafluencer.delete()

            return jsonify({
                "success": True,
                "delete": insta_id
            })

        except BaseException:

            abort(404)

    # Error Handling
    '''
    Example error handling for unprocessable entity
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 422,
                        "message": "unprocessable"
                        }), 422

    '''
    @TODO implement error handlers using the @app.errorhandler(error) decorator
        each error handler should return (with approprate messages):
                 jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    '''

    '''
    @TODO implement error handler for 404
        error handler should conform to general task above
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error'
        }), 500

    '''
    @TODO implement error handler for AuthError
        error handler should conform to general task above
    '''

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
