import numpy as np
import pandas as pd
import re

from app import db
from models import Crime

def load_data(file_name):
    return pd.read_csv(file_name)

data = load_data('../SPD_Reports.csv')

def ingest_data(data):
    i = 0
    for idx, values in data.iterrows():
        val = values.values

        if type(val[3]) != str or type(val[2]) != str:
            continue

        if type(val[4]) != str:
            val[4] = None

        m = re.search('(?<=T).*?(?=:)', val[3])
        time = int(m.group(0))

        crime = Crime(val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7], val[8], float(val[9]), float(val[10]), time)

        db.session.add(crime)

        i += 1
        if i % 1000 == 0:
            db.session.commit()
            db.session.close()
            p = i / 700000.
            print str(p) + '%'




ingest_data(data)
