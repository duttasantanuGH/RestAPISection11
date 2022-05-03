from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    storeID = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')


    def __init__(self, name, price, storeID):
        self.name = name
        self.price = price
        self.storeID = storeID

    def json(self):
        return {'id': self.id, 'name': self.name, 'price': self.price, 'storeID': self.storeID}

    @classmethod
    def findByName(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def findAll(cls):
        cls.query.all()

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()