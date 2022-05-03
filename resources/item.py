from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field is mandatory, please enter price in $ XX.YY format')
    parser.add_argument('storeID',
                        type=int,
                        required=True,
                        help='Every item will need store ID')

    @jwt_required()
    def get(self, name):
        item = ItemModel.findByName(name)
        if item:
            return item.json()
        else:
            return {'message': '[INFO] Item with name {} is not found'.format(name)}, 404

    def post(self, name):
        if ItemModel.findByName(name):
            return {'message': '[INFO] The item {} already exists'.format(name)}, 400
        else:
            data = Item.parser.parse_args()
            item = ItemModel(name, data['price'], data['storeID'])
            item.saveToDB()
            return {'message': '[INFO] The item {} with price {} in store with ID {} created'.
                format(name, data['price'], data['storeID'])}, 201

    def delete(self, name):
        item = ItemModel.findByName(name)
        if item:
            item.deleteFromDB()
            return {'message': '[INFO] The item {} is deleted'.format(name)}, 202
        else:
            return {'message': '[INFO] Item with name {} is not found'.format(name)}, 404


    def put(self, name):
        item = ItemModel.findByName(name)
        data = Item.parser.parse_args()

        if item:
            item.price = data['price']
            item.storeID = data['storeID']
            message = {'message': '[INFO] the price for Item with name {} is updated with the price {} and storeID {}'
                .format(name, data['price'], data['storeID'])}
        else:
            item = ItemModel(name, data['price'], data['storeID'])
            message = {'message': '[INFO] Item with name {} and price {} in store with ID {} is created'.
                format(name, data['price'], data['storeID'])}

        item.saveToDB()
        return message

class ItemList(Resource):
    def get(self):
        items = []
        rows = ItemModel.query.all() # changed
        #rows = ItemModel.findAll() # changed
        for row in rows:
            items.append(row.json())
        #return {'items': [item.json() for item in ItemModel.query.all()]}, 201
        return {'items': items}, 201
