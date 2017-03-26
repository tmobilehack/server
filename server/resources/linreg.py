from flask_restful import reqparse, Resource
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from random import random
from sklearn import datasets, linear_model
import numpy as np

engine = create_engine('postgresql://ubuntu:password@localhost/tmobilehack')

conn = engine.connect()

class LinReg(object):
    @staticmethod
    def train():
        locations = []

        stmt = text('SELECT latitude, longitude\
        FROM crimes\
        WHERE offense_start_date >= :sdate\
        AND offense_start_date <= :edate')

        stmt = stmt.bindparams(sdate = "2009-01-01", edate = "2009-01-05")
        points = conn.execute(stmt)

        for res in points:
            locations.append((res[0], res[1]))
        print "NUM LOCATIONS"
        print len(locations)
        crimeTypesStmt = text('SELECT DISTINCT offense_description FROM crimes')
        types = conn.execute(crimeTypesStmt)
        crimeTypes = {}
        counter = 0
        for row in types:
            crimeTypes[row[0]] = counter
            counter += 1
        print crimeTypes

        X = []
        y = []

        # For each chosen location, compute features and add to dataset
        for location in locations:
            timeRanges = [("2013-09-20", "2014-09-19"), ("2014-09-20", "2015-09-19")]
            features = []

            lat = location[0]
            lon = location[1]
            RADIUS = 0.25
            maxLat = lat + (RADIUS / 111.2)
            minLat = lat - (RADIUS / 111.2)
            maxLong = lon + (RADIUS / 75.1)
            minLong = lon - (RADIUS / 75.1)
            for timeRange in timeRanges:
                thisTimeFeatures = [0] * len(crimeTypes)

                stmt = text('SELECT offense_description, COUNT(id) FROM crimes\
                WHERE latitude < :upperLat AND latitude > :lowerLat\
                AND longitude < :upperLong AND longitude > :lowerLong\
                AND offense_start_date >= :sdate\
                AND offense_start_date <= :edate\
                AND (75.1 * (longitude - :ptLong))^2 + (111.2 * (latitude - :ptLat)) ^ 2 < :squaredRadius\
                GROUP BY offense_description')

                stmt = stmt.bindparams(upperLat = maxLat, lowerLat = minLat, upperLong = maxLong, lowerLong = minLong,
                 ptLat = lat, sdate = timeRange[0], edate = timeRange[1], ptLong = lon, squaredRadius = RADIUS ** 2)
                res = conn.execute(stmt)
                for row in res:
                    crimeTypeIndex = crimeTypes[row[0]]
                    thisTimeFeatures[crimeTypeIndex] = row[1]
                #print thisTimeFeatures
                features = features + thisTimeFeatures

            X.append(features)

            # Total number of crimes within 1 km
            # in the past year
            stmt = text('SELECT COUNT(id) FROM crimes\
            WHERE latitude < :upperLat AND latitude > :lowerLat\
            AND longitude < :upperLong AND longitude > :lowerLong\
            AND offense_start_date >= :sdate\
            AND offense_start_date <= :edate\
            AND (75.1 * (longitude - :ptLong))^2 + (111.2 * (latitude - :ptLat)) ^ 2 < :squaredRadius')
            stmt = stmt.bindparams(upperLat = maxLat, lowerLat = minLat, upperLong = maxLong, lowerLong = minLong,
             ptLat = lat, sdate = "2015-09-20", edate = "2016-09-19", ptLong = lon, squaredRadius = RADIUS ** 2)
            countRes = conn.execute(stmt)
            numCrimes = 0
            #print "TOTAL NUMBER OF CRIMES"
            for row in countRes:
                #print row
                numCrimes = row[0]
            y.append(numCrimes)
            print numCrimes

        cutoff = 4 * len(X) / 5
        X_train = X[:cutoff]
        X_test = X[cutoff:]
        y_train = X[:cutoff]
        y_test = X[cutoff:]

        print X_train
        print y_train
        regr = linear_model.LinearRegression()
        regr.fit(X_train, y_train)
        print "Coefficients"
        print regr.coef_


        return {
            'scores': scores,
            'crimes': {
            'home': responsex,
            'vehicle': responsez,
            'walk': responsey
            }
        }

LinReg.train()
