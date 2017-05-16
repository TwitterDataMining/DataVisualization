from dataVisualization import db


class Example(db.Document):
    name = db.StringField()


class UserData(db.Document):
    user_id = db.StringField()
    tweets = db.StringField()
