from app import db

class Crime(db.Model):
    __tablename__ = 'crimes'

    id = db.Column(db.Integer, primary_key=True)
    offense_type = db.Column(db.String())
    offense_description = db.Column(db.String())
    report_date = db.Column(db.String())
    offense_start_date = db.Column(db.String())
    offense_end_date = db.Column(db.String())
    block = db.Column(db.String())
    district = db.Column(db.String())
    beat = db.Column(db.String())
    census_tract = db.Column(db.String())
    longitude = db.Column(db.String())
    latitude = db.Column(db.String())

    def __init__(self,
                offense_type,
                offense_description,
                report_date,
                offense_start_date,
                offense_end_date,
                block,
                district,
                beat,
                census_tract,
                longitude,
                latitude):

        self.offense_type = offense_type
        self.offense_description = offense_description
        self.report_date = report_date
        self.offense_start_date = offense_start_date
        self.offense_end_date = offense_end_date
        self.block = block
        self.district = district
        self.beat = beat
        self.census_tract = census_tract
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self):
        return '<date {}>'.format(self.report_date)
