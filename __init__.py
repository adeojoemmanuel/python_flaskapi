from api import *


api.add_resource(CreateUser, '/CreateUser')
api.add_resource(AuthenticateUser, '/AuthenticateUser')
api.add_resource(AddItem, '/AddItem')
api.add_resource(GetAllItems, '/GetAllItems')
api.add_resource(Test, '/test')
api.add_resource(ReturnResponse, '/testResponse')
api.add_resource(newData, '/insertData')
api.add_resource(updateData, '/updateData')

if __name__ == '__main__':
    app.run(debug=True)