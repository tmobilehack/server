import numpy as np
import pandas as pd

from app import db
from models import Crime

def load_data(file_name):
    return pd.read_csv(file_name)

data = load_data('../SPD_Reports.csv')

def ingest_data(data):
    i = 0
    for idx, values in data.iterrows():
        val = values.values

        crime = Crime(val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7], val[8], val[9], val[10])

        i += 1
        print i
        if i % 1000 == 0:
            print $'${i}%'

        db.session.add(crime)
        db.session.commit()
        db.session.close()

ingest_data(data)
