import dill

from db import db


class ScorerModel(db.Model):
    __tablename__ = 'scorers'

    # id = db.Column(db.Integer, primary_key=True)
    scorer_id = db.Column(db.String(50), primary_key=True)
    scorer_obj = db.Column(db.PickleType(pickler=dill))
    scorer_summary = db.Column(db.String(200))
    scorer_uploaded = db.Column(db.String(20))

    def __init__(self, scorer_id, scorer_obj, scorer_summary, scorer_uploaded=None):
        self.scorer_id = scorer_id
        self.scorer_obj = scorer_obj
        self.scorer_summary = scorer_summary
        self.scorer_uploaded = scorer_uploaded

    def json(self):
        return {k: getattr(self, k) for k in ['scorer_id', 'scorer_summary', 'scorer_uploaded']}

    @classmethod
    def find_by_scorer_id(cls, scorer_id):
        return cls.query.filter_by(scorer_id=scorer_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all_scorers(cls):
        return cls.query.all()
