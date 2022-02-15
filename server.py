from itertools import count
from os import abort
from mock_data import catalog
from flask import Flask, abort
from about_me import me 
import json 

#create the server/app
app = Flask("server")

@app.route("/", methods=["get"])
def home_page():
    return "Under Construction"

@app.route("/about")
def about_me():
    return "Nicholas Lucien"

@app.route("/test")
def test():
    return "Simple Test"

@app.route("/myaddress")
def get_address():
    address = me["address"]
    # return address["street"]
    return f"{address['street']} {address['city']}"

#start the server 

@app.route("/api/catalog")
def get_catalog():
    return json.dumps(catalog)

#get /api/catalog/count
@app.route("/api/catalog/count")
def get_catalogcount():     
    count = len(catalog)
    return json.dumps(count)

@app.route("/api/catalog/sum")
def get_sum():
    total = 0
    for prod in catalog:
        total += prod["price"]

    res = "$" + str(total)
    return json.dumps(res)

@app.route("/api/product/<id>")
def get_product(id):
    for prod in catalog:
        if id == prod["_id"]:
            return json.dumps(prod)
    return abort(404) # 400 not found

@app.route("/api/product/most_expensive")
def get_most_expensive():
    pivot = catalog[0]
    for prod in catalog:
        if prod["price"] > pivot["price"]:
            pivot = prod
    return json.dumps(pivot)


#start the server
app.run(debug=True)