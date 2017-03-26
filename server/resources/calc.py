from flask_restful import reqparse, Resource
from sqlalchemy.sql import text
from random import random
from models import Crime

from copy import copy

from app import db

parser = reqparse.RequestParser()
parser.add_argument('latitude', type=float)
parser.add_argument('longitude', type=float)

class Test(Resource):
    def get(self):

        return {
    "crimes": {
        "home": [
            {
                "beat": "99",
                "block": "82XX BLOCK OF S 114 ST",
                "census_tract": "NaN",
                "district": "99",
                "hour": 6,
                "latitude": 47.500843048,
                "longitude": -122.228408813,
                "offense_description": "CAR PROWL",
                "offense_end_date": "2016-02-11T07:40:00",
                "offense_report_date": "2016-02-11T12:46:00",
                "offense_start_date": "2016-02-11T06:40:00",
                "offense_type": "THEFT-CARPROWL"
            }
        ],
        "vehicle": [
            {
                "beat": "99",
                "block": "82XX BLOCK OF S 114 ST",
                "census_tract": "NaN",
                "district": "99",
                "hour": 6,
                "latitude": 47.500843048,
                "longitude": -122.228408813,
                "offense_description": "CAR PROWL",
                "offense_end_date": "2016-02-11T07:40:00",
                "offense_report_date": "2016-02-11T12:46:00",
                "offense_start_date": "2016-02-11T06:40:00",
                "offense_type": "THEFT-CARPROWL"
            }
        ],
        "walk": []
    },
    "scores": {
        "home": 0.0004,
        "vehicle": 0.0032258064516129032,
        "walk": 0.0
    }
}

class Calc(Resource):
    def get(self):

        args = parser.parse_args()

        scores = {}

        conn = db.get_engine().connect()

        lat = args.latitude
        lon = args.longitude

        RADIUS = 0.25
        maxLat = lat + (RADIUS / 111.2)
        minLat = lat - (RADIUS / 111.2)
        maxLong = lon + (RADIUS / 75.1)
        minLong = lon - (RADIUS / 75.1)
        stmt = text('SELECT * FROM crimes\
        WHERE latitude < :upperLat AND latitude > :lowerLat\
        AND longitude < :upperLong AND longitude > :lowerLong\
        AND offense_start_date > :sdate\
        AND (75.1 * (longitude - :ptLong))^2 + (111.2 * (latitude - :ptLat)) ^ 2 < :squaredRadius')

        stmt = stmt.bindparams(upperLat = maxLat, lowerLat = minLat, upperLong = maxLong, lowerLong = minLong,
         ptLat = lat, sdate = "2015-09-19", ptLong = lon, squaredRadius = RADIUS ** 2)
        homeRes = conn.execute(stmt)

        walkingStatement = text('SELECT * FROM crimes\
            WHERE latitude < :upperLat AND latitude > :lowerLat\
            AND longitude < :upperLong AND longitude > :lowerLong\
            AND offense_start_date > :sdate\
            AND (75.1 * (longitude - :ptLong))^2 + (111.2 * (latitude - :ptLat)) ^ 2 < :squaredRadius\
            AND (offense_description = :assault\
            OR offense_description = :threats\
            OR offense_description = :pickpocket\
            OR offense_description = :pursesnatch\
            OR offense_description = :homicide\
            OR offense_description = :dui)')
        walkingStatement = walkingStatement.bindparams(upperLat = maxLat, lowerLat =    minLat, upperLong = maxLong, lowerLong = minLong, sdate = "2015-09-19",
        ptLat = lat, ptLong = lon, squaredRadius = RADIUS ** 2, assault = "ASSAULT", threats = "THREATS", pickpocket = "PICKPOCKET", pursesnatch = "PURSE SNATCH", homicide = "HOMICIDE", dui = "DUI")
        walkingRes = conn.execute(walkingStatement)

        parkingStatement = text('SELECT * FROM crimes\
            WHERE latitude < :upperLat AND latitude > :lowerLat\
            AND longitude < :upperLong AND longitude > :lowerLong\
            AND offense_start_date > :sdate\
            AND (75.1 * (longitude - :ptLong))^2 + (111.2 * (latitude - :ptLat)) ^ 2 < :squaredRadius\
            AND (offense_description = :carprowl\
            OR offense_description = :vehicletheft\
            OR offense_description = :biketheft)')
        parkingStatement = parkingStatement.bindparams(upperLat = maxLat, lowerLat =    minLat, upperLong = maxLong, lowerLong = minLong, sdate = "2015-09-19",
        ptLat = lat, ptLong = lon, squaredRadius = RADIUS ** 2, carprowl = "CAR PROWL", vehicletheft = "VEHICLE THEFT", biketheft = "BIKE THEFT")
        parkingRes = conn.execute(parkingStatement)

        responsex = []
        responsey = []
        responsez = []

        for res1 in homeRes:
            x = list(res1)
            x[-1] = x[-1].strftime('%Y-%m-%dT%H:%M:%S')
            try:
                x[-2] = x[-2].strftime('%Y-%m-%dT%H:%M:%S')
            except:
                pass
            try:
                x[-3] = x[-3].strftime('%Y-%m-%dT%H:%M:%S')
            except:
                pass
            dic = {}
            dic['offense_type'] = x[1]
            dic['offense_description'] = x[2]
            dic['block'] = x[3]
            dic['district'] = x[4]
            dic['beat'] = x[5]
            dic['census_tract'] = x[6]
            dic['hour'] = x[7]
            dic['latitude'] = x[8]
            dic['longitude'] = x[9]
            dic['offense_end_date'] = x[10]
            dic['offense_start_date'] = x[11]
            dic['offense_report_date'] = x[12]
            responsex.append(dic)
        for res2 in parkingRes:
            z = list(res2)
            z[-1] = z[-1].strftime('%Y-%m-%dT%H:%M:%S')
            try:
                z[-2] = z[-2].strftime('%Y-%m-%dT%H:%M:%S')
            except:
                pass
            try:
                z[-3] = z[-3].strftime('%Y-%m-%dT%H:%M:%S')
            except:
                pass
            dic = {}
            dic['offense_type'] = z[1]
            dic['offense_description'] = z[2]
            dic['block'] = z[3]
            dic['district'] = z[4]
            dic['beat'] = z[5]
            dic['census_tract'] = z[6]
            dic['hour'] = z[7]
            dic['latitude'] = z[8]
            dic['longitude'] = z[9]
            dic['offense_end_date'] = z[10]
            dic['offense_start_date'] = z[11]
            dic['offense_report_date'] = z[12]
            responsez.append(dic)
        for res3 in walkingRes:
            y = list(res3)
            y[-1] = y[-1].strftime('%Y-%m-%dT%H:%M:%S')
            try:
                y[-2] = y[-2].strftime('%Y-%m-%dT%H:%M:%S')
            except:
                pass
            try:
                y[-3] = y[-3].strftime('%Y-%m-%dT%H:%M:%S')
            except:
                pass
            dic = {}
            dic['offense_type'] = y[1]
            dic['offense_description'] = y[2]
            dic['block'] = y[3]
            dic['district'] = y[4]
            dic['beat'] = y[5]
            dic['census_tract'] = y[6]
            dic['hour'] = y[7]
            dic['latitude'] = y[8]
            dic['longitude'] = y[9]
            dic['offense_end_date'] = y[10]
            dic['offense_start_date'] = y[11]
            dic['offense_report_date'] = y[12]
            responsey.append(dic)

        print 'sending...'

        scores['home'] = (len(responsex)/2500.)
        scores['vehicle'] = (len(responsez)/310.)
        scores['walk'] = (len(responsey)/450.)

        try:
            responsex = responsex[:100]
        except:
            pass

        try:
            responsez = responsez[:100]
        except:
            pass

        try:
            responsey = responsey[:100]
        except:
            pass

        return {
            'scores': scores,
            'crimes': {
            'home': responsex,
            'vehicle': responsez,
            'walk': responsey
            }
        }

        # crimes_db = Crime.query.filter_by('latitude' < 47.6).limit(5).all()

        # print db.execute('select * from crimes limit 1')

        # crimes = [x.__dict__ for x in crimes_db]
        # for crime in crimes:
        #     del crime['_sa_instance_state']
        #
        # print crimes[0]
        # return {'score': score, 'crimes': crimes}
