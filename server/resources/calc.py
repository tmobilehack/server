from flask_restful import reqparse, Resource
from random import random
from models import Crime

class Calc_danger(Resource):
    def get(self):

        score = random()
        crimes = []
        # crimes.append(Crime.query.limit(5).all())

        return {'score': score, 'crimes': crimes}

        # calc score

        # return {score, crimes: {...}}
