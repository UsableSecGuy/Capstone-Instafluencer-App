import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    @TODO uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''
    # db_drop_and_create_all()

    ## ROUTES
    '''
    @TODO implement endpoint
        GET /drinks
            it should be a public endpoint
            it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    '''
    @app.route('/drinks')
    def get_drinks():
        try:

            all_drinks = Drink.query.order_by('id').all()

            formatted_drinks=[drink.short() for drink in all_drinks]

            return jsonify({
            'success': True,
            'drinks': formatted_drinks
            })
        except:
            abort(404)

    '''
    @TODO implement endpoint
        GET /drinks-detail
            it should require the 'get:drinks-detail' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
            where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    '''
    @app.route('/drinks-detail')
    @requires_auth('get:drinks-detail')
    def get_drinks_detail(jwt):
        try:

            all_drinks = Drink.query.order_by('id').all()

            formatted_drinks=[drink.long() for drink in all_drinks]

            return jsonify({
            'success': True,
            'drinks': formatted_drinks
            })
        except:
            abort(404)


    '''
    @TODO implement endpoint
        POST /drinks
            it should create a new row in the drinks table
            it should require the 'post:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the newly created drink
            or appropriate status code indicating reason for failure
    '''

    @app.route('/drinks', methods=['POST'])
    @requires_auth('post:drinks')
    def post_drinks(jwt):
        #get request from the client
        body = request.get_json()

        #get info from the body and if nothing there set it to None
        new_title = body.get('title', None)
        new_recipe = body.get('recipe', None)
        print(new_recipe)


        try:


            if isinstance(new_recipe, dict):
                new_recipe = [new_recipe]


            #sql can't store objects so you have to dump json with
            #for recipe so it will convert to a string which json can store
            drink = Drink(title = new_title, recipe = json.dumps(new_recipe))

            drink.insert()

            return jsonify({
            "success": True,
            "drinks": [drink.long()]
            })

        except:
            abort(400)


    '''
    @TODO implement endpoint
        PATCH /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
            or appropriate status code indicating reason for failure
    '''

    @app.route('/drinks/<int:drink_id>', methods=['PATCH'])
    @requires_auth('patch:drinks')
    def update_drink(jwt, drink_id):
        try:
            drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

            #check if drink even exists
            if drink is None:
                abort(404)

            #get payload for update
            body = request.get_json()

            #see what's being updated and change value
            if "title" in body:
                #get info from the body and if nothing there set it to None
                new_title = body.get('title', None)

                drink.title = new_title

            if "recipe" in body:
                new_recipe = body.get('recipe', None)
                drink.recipe = json.dumps(new_recipe)

            drink.update()

            return jsonify({
            "success": True,
            "drinks": [drink.long()]
            })

        except:
            abort(404)

    '''
    @TODO implement endpoint
        DELETE /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''

    @app.route('/drinks/<int:drink_id>', methods=['DELETE'])
    @requires_auth('delete:drinks')
    def delete_drink(jwt,drink_id):
        try:
            drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

            if drink is None:
                abort(404)

            #delete question from db
            drink.delete()

            return jsonify({
            "success": True,
            "delete": drink_id
            })

        except:

            abort(404)



    ## Error Handling
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
