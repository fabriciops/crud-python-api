from datetime import datetime, timedelta
import json
from flask import Flask, Response, jsonify, request, make_response
import numpy as np
import config
import mysql.connector

app = Flask(__name__)

host = config.host
user = config.user
passwd = config.passwd
database = config.database
secretkey = config.secretkey

db = mysql.connector.connect(
        host =   host,
        user =   user,
        passwd =  passwd,
        database = database
)

@app.route("/", methods=["GET"])
def getAllProduct():

    if(secretkey == config.secretkey):

        cursor = db.cursor()
        sql = "SELECT id, product_name, img from product"
        cursor.execute(sql)
        product = cursor.fetchall()

        if product is not None:

            response = make_response(jsonify(product, 200))

            return response
            
        else:
            response = make_response(jsonify({"message": "Product is Update success"}, 403))
            return response

@app.route("/create_product", methods=["POST"])
def insertProduct():

    if(secretkey == config.secretkey):

        req = request.get_json()
        req = req[0]

        if req:
            
            resName = req.get("name")
            resImg = req.get("img")

            now = datetime.now()
            updateNow = str(now)
            
            data = (resName, resImg, updateNow, updateNow)
        
        else:
            response = make_response(jsonify({"message":"POST without object or invalid"}, 403))
            return response


        if data:
            try:

                cursor = db.cursor()
                sql = "INSERT INTO product (product_name, img, creat_at, update_at) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, data)
                result = db.commit()

                if result is None:
    
                    response = make_response(jsonify({"message":"Product Update created"}, 200))                    
                    return response
                else:
                    response = make_response(jsonify({"message":"Product is not created"}, 403))
                    return response
                    

            finally:
                cursor.close()

def getProductById(id):

        cursor = db.cursor()
        sql = "SELECT * from product WHERE id = {}".format(id)
        cursor.execute(sql)
        product = cursor.fetchall()

        if product:
            return product
            
        else:
            return False

@app.route("/update", methods=["PUT"])
def updateProduct():

    req = request.get_json()
    req = req[0]
    resId = req.get("id")
    
    lastUpdateProduct = veryfiProductUpdateAt(resId)

    if lastUpdateProduct is True:
        updateProductDb(req)
        response = make_response(jsonify({"id": resId, "message": "Product Update success"}, 200))
        return response
    else:
        response = make_response(jsonify({"message":"Product is not update"}, 403))
        return response


def updateProductDb(req):

    req = request.get_json()
    req = req[0]
    resId = req.get("id")
    resName = req.get("name")
    resImg = req.get("img")

    now = datetime.now()
    updateNow = str(now)
    
    data = (resName, resImg, updateNow,resId)

    if data:
        try:

            cursor = db.cursor()
            sql = "UPDATE product SET product_name = %s, img = %s, update_at = %s WHERE id = %s"
            cursor.execute(sql, data)
            

        finally:
            cursor.close()
            
def veryfiProductUpdateAt(id):

    product = getProductById(id)
    lastUpdate = product[0][4]

    d = datetime.today() - timedelta(hours=0, minutes=10)

    if d > lastUpdate:
        return True
    else:
        return False
        
if __name__ == '__main__':
    
    app.run(debug=True)
