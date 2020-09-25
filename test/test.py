
import requests, jsonify, json
import make_response

class Test():

    def getAllProduct(self):

        responseProduct = requests.get('http://127.0.0.1:5000/')

        if(responseProduct and responseProduct.status_code == 200):
            
            return responseProduct
        else:
            response = make_response(jsonify({"message": "AnyOne Product"}, 403))
            return response
    
    def create_product(self, nome, img):

        dataUser = [{"name": nome, "img": img}]
    
        responseProductCreate = requests.post('http://127.0.0.1:5000/create_product', json=dataUser)
        
        if(responseProductCreate and responseProductCreate.status_code == 200):
            return responseProductCreate
            
        else:
    
            response = make_response(jsonify({"message":"Product is not created"}, 403))
            return response
    
    def updateProduct(self, id, nome, img):
    
        dataUser = [{"id": id, "name": nome, "img": img}]
    
        responseProductCreate = requests.put('http://127.0.0.1:5000/update', json=dataUser)
        
        if(responseProductCreate and responseProductCreate.status_code == 200):
            
            return responseProductCreate
            
        else:
            
            response = make_response(jsonify({"message":"Product is not created"}, 403))
            return response

    def testUpdateRequest(self, id, nome, img):
    
        dataUser = [{"id": id, "name": nome, "img": img}]
        
        responseProductCreate = requests.put('http://127.0.0.1:5000/update', json=dataUser)
        
        if(responseProductCreate and responseProductCreate.status_code == 200):

            responseProductCreate = requests.put('http://127.0.0.1:5000/update', json=dataUser)
            
            if(responseProductCreate and responseProductCreate.status_code == 200):
                return responseProductCreate
            
            else:
                
                response = make_response(jsonify({"message":"Product is not created"}, 403))
                return response
            
        else:
            
            response = make_response(jsonify({"message":"Product is not created"}, 403))
            return response

test = Test()

getAll = test.getAllProduct()
print("All Product", getAll)

creatNew = test.create_product("teste", "Jimmi.jpg")
print("Creat a New Product:", creatNew)


updateProduct = test.updateProduct("1","2020", "Jimmi.jpg")
print("Update Product", updateProduct)

updateProduct = test.testUpdateRequest("1","TestRequest", "Jimmi.jpg")
print("Update Product", updateProduct)



