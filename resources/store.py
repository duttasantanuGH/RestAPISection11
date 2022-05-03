from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.findByName(name)
        if store:
            return store.json(), 200
        return {'message': 'A store with name {} does not exist'.format(name)}, 404

    def post(self, name):
        store = StoreModel.findByName(name)
        if store:
            return {'message': 'A store with name {} already exist'.format(name)}, 400
        store = StoreModel(name)
        try:
            store.saveToDB()
        except:
            return {'message': 'An internal server error occured while saving Store data with ID {}. '
                               'Please after sometime.'.format(name)}, 500
        return {'message': 'A store with name {} created successfully'.format(name)}, 201

    def delete(self, name):
        store = StoreModel.findByName(name)
        if store:
            try:
                store.deleteFromDB()
                return {'message': 'A store with name {} deleted'.format(name)}, 200
            except:
                return {'message': 'An internal server error occured while deleting Store data with name {}.'
                                   'Please after sometime.'.format(name)}, 500
        else:
            return {'message': 'A store with name {} does not exist'.format(name)}, 404


class StoreList(Resource):
    def get(self):
        storeList =[]
        #rows = StoreModel.findAll()
        rows = StoreModel.query.all()
        for row in rows:
            storeList.append(row.json())
        return {'storeList': storeList}, 201
        #return {'storeList': [store.json() for store in StoreModel.query.all()]}
