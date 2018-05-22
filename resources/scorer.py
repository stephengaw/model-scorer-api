import dill
import numpy as np
import pandas as pd
from flask import request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
from flask_restful import Resource, reqparse

from models.scorer import ScorerModel


class Scorer(Resource):
    @jwt_optional
    def get(self, scorer_id):
        user_id = get_jwt_identity()
        scorer = ScorerModel.find_by_scorer_id(scorer_id)
        if scorer:
            if user_id:
                return scorer.json(), 200
            else:
                return {
                           'scorer': scorer.scorer_id,
                           'message': 'More details available with authentication.'
                       }, 200
        return {'message': 'Cannot find scorer_id.'}, 404

    @fresh_jwt_required
    def post(self, scorer_id):
        if ScorerModel.find_by_scorer_id(scorer_id):
            return {'message': "A scorer with scorer_id '{}' already exists.".format(scorer_id)}, 400

        raw_data = request.get_data()

        try:
            scorer_obj = dill.loads(raw_data)
        except:
            return {'message': "Unable to read serialised scorer."}, 400

        scorer = ScorerModel(scorer_id, scorer_obj, str(scorer_obj))

        try:
            scorer.save_to_db()
        except:
            return {'message': "An error occurred while trying to insert the item."}, 500

        return scorer.json(), 201

    @fresh_jwt_required
    def put(self, scorer_id):
        data = request.get_data()
        scorer_obj = dill.loads(data)

        scorer = ScorerModel.find_by_scorer_id(scorer_id)

        if scorer is None:
            scorer = ScorerModel(scorer_id, scorer_obj, str(scorer_obj))
        else:
            scorer.scorer_obj = scorer_obj
            scorer.scorer_summary = str(scorer_obj)

        try:
            scorer.save_to_db()
        except:
            return {'message': "An error occurred while trying to save the item"}, 500

        return scorer.json()

    @fresh_jwt_required
    def delete(self, scorer_id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privileges required.'}, 401

        scorer = ScorerModel.find_by_scorer_id(scorer_id)
        if scorer:
            scorer.delete_from_db()
            return {'message': "Scorer '{}' deleted.".format(scorer_id)}, 200
        return {'message': 'Cannot find scorer_id.'}, 404


class ScorerList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        scorers = ScorerModel.find_all_scorers()

        if user_id:
            return {'scorers': [scorer.json() for scorer in scorers]}, 200
        return {
                   'scorers': [scorer.scorer_id for scorer in scorers],
                   'message': 'More details available with authentication.'
               }, 200


class ScorerPredictWithList(Resource):
    @jwt_required
    def post(self, scorer_id):

        parser = reqparse.RequestParser()
        parser.add_argument('features',
                            required=True,
                            action='append',  # allows lists to be passed.
                            help='This field cannot be blank')

        data = parser.parse_args()

        scorer = ScorerModel.find_by_scorer_id(scorer_id)
        if scorer:
            try:
                X = np.array(data['features']).reshape(1, -1)
            except Exception:
                return {'message': 'Invalid features set.'}, 400

            y = scorer.scorer_obj.predict(X).tolist()  # unpack returned array to individual prediction
            return {'prediction': y}, 200
        else:
            return {'message': 'Cannot find scorer_id.'}, 404


class ScorerPredictWithDict(Resource):
    @jwt_required
    def post(self, scorer_id):

        parser = reqparse.RequestParser()
        parser.add_argument('features',
                            required=True,
                            type=dict,
                            help='This field cannot be blank')
        data = parser.parse_args()

        scorer = ScorerModel.find_by_scorer_id(scorer_id)
        if scorer:
            try:
                X = pd.DataFrame(data['features'])
            except Exception:
                return {'message': 'Invalid features set.'}, 400

            y = scorer.scorer_obj.predict(X).tolist()  # unpack returned array to individual prediction
            return {'prediction': y}, 200
        else:
            return {'message': 'Cannot find scorer_id.'}, 404


class ScorerTransformWithDict(Resource):
    @jwt_required
    def post(self, scorer_id):

        parser = reqparse.RequestParser()
        parser.add_argument('features',
                            required=True,
                            type=dict,
                            help='This field cannot be blank')
        data = parser.parse_args()

        scorer = ScorerModel.find_by_scorer_id(scorer_id)
        if scorer:
            try:
                X = pd.DataFrame(data['features'])
            except Exception:
                return {'message': 'Invalid features set.'}, 400

            y = scorer.scorer_obj.transform(X).tolist()  # unpack returned array to individual prediction
            return {'transformation': y}, 200
        else:
            return {'message': 'Cannot find scorer_id.'}, 404
