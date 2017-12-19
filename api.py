from flask import Flask
# import pymysql as MySQL
from flask_restful import Resource, Api
from flask_restful import reqparse
# from flask.ext.mysql import MySQL
from flaskext.mysql import MySQL
from flask import Flask, jsonify, request, abort
import config 
import sys
import iohandler
# from __future__ import unicode_literals
# from plib import Api, Resource, cors
# from . import  api, resource, cors
# from .plib import Api, Resource, cors
from flask_cors import CORS

connection = config.connection()

# return {'Allow' : 'PUT' }, 200, \
    # { 'Access-Control-Allow-Origin': '*', \
      # 'Access-Control-Allow-Methods' : 'PUT,GET' }

mysql = MySQL()
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

dbconn = connection.startConnection()

handler = iohandler.Ioapi()

api = Api(app)
# CORS(app, resources={r"/*": {"origins": "*"}})

class AuthenticateUser(Resource):
    def post(self):
        try:
            req_data = request.get_json(force=True)
            __name = req_data['name']
            __keyword = req_data['keyword']

            # conn = mysql.connect()
            cursor = dbconn.cursor()
            cursor.callproc('userAuth',(_userEmail,))
            data = cursor.fetchall()

            
            if(len(data)>0):
                if(str(data[0][2])==_userPassword):
                    # return {'status':200,'UserId':str(data[0][0])}
                    return jsonify({'status' : '200', 'UserId':str(data[0][0])})
                else:
                    # return {'status':100,'message':'Authentication failure'}
                    return jsonify({'status' : '201', 'message':'Authentication failure'})

        except Exception as e:
            return {'error': str(e)}


class GetAllItems(Resource):
    def post(self):
        try: 
            req_data = request.get_json(force=True)
            _userId = req_data['id']

            # conn = mysql.connect()
            cursor = dbconn.cursor()
            cursor.callproc('users',(_userId,))
            data = cursor.fetchall()

            items_list=[];
            for item in data:
                i = {
                    'Id':item[0],
                    'Item':item[1]
                }
                items_list.append(i)

            # return {'StatusCode':'200','Items':items_list}
            return jsonify({'StatusCode' : '200', 'Items':items_list})

        except Exception as e:
            # return {'error': str(e)}
            return jsonify({'error': str(e)})

class AddItem(Resource):
    def post(self):
        try: 
            req_data = request.get_json(force=True)
            _userId = req_data['id']
            _item = req_data['item']

            print _userId;

            # conn = mysql.connect()
            cursor = dbconn.cursor()
            cursor.callproc('items',(_userId,_item))
            data = cursor.fetchall()

            conn.commit()
            # return {'StatusCode':'200','Message': 'Success'}
            return jsonify({'StatusCode':'200','Message': 'Success'})

        except Exception as e:
            # return {'error': str(e)}
            return jsonify({'error': str(e)})
        
                

class CreateUser(Resource):
    def post(self):
        try:
            # Parse the arguments
            # parser = reqparse.RequestParser()
            # parser.add_argument('email', type=str, help='Email address to create user')
            # parser.add_argument('password', type=str, help='Password to create user')
            # args = parser.parse_args()
            req_data = request.get_json(force=True)
            _userEmail = req_data['email']
            _userPassword = req_data['password']

            # conn = mysql.connect()
            cursor = dbconn.cursor()
            cursor.callproc('spCreateUser',(_userEmail,_userPassword))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                # return {'StatusCode':'200','Message': 'User creation success'}
                return jsonify({'StatusCode':'200','Message': 'User creation success'})
            else:
                # return {'StatusCode':'1000','Message': str(data[0])}
                return jsonify({'StatusCode':'1000','Message': str(data[0])})

        except Exception as e:
            # return {'error': str(e)}
            return jsonify({'error': str(e)})

class Test(Resource):
    def post(self):
        return jsonify({'success': "working"})

class ReturnResponse(Resource):
    def post(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('name', type=str, help='input your name')
        # parser.add_argument('keyword', type=str, help='input your keyword')
        # args = parser.parse_args()

        # args is use to get from url search = request.args.get("search")
        # email = request.form.get('email') form is use to get form input 

        req_data = request.get_json(force=True)
        # data = request.data     is already depreciated

        __name = req_data['name']
        __keyword = req_data['keyword']

        return jsonify({'success' : 'true', 'name' : __name, 'keyword' : __keyword})

class newData(Resource):
    def post(self):
        req_data = request.get_json(force=True)
        fn = req_data['firstName']
        ln = req_data['lastName']
        pn = req_data['phoneNumber']
        nn = req_data['nickName']


        query = handler.insert('datas', fn, ln, pn, nn)

        if (query == "success"):
            return jsonify({'success' : 'true', 'message' : 'data inserted'})
            # return query
        else:
            return jsonify({'success' : 'false', 'message' : 'data not inserted'})
            # return "error inserting"

class newInsert(Resource):
    def post(self):
        req_data = request.get_json(force=true)

        query = handler.insertArr(arrayVal, arrayTable, 'datas')

        if (query == "success"):
            return jsonify({'success' : 'true', 'message' : 'data inserted'})
            # return query
        else:
            return jsonify({'success' : 'false', 'message' : 'data not inserted'})
            # return "error inserting"

        
        
        