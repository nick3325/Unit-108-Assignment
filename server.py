
from random import random
from mock_data import catalog
from flask import Flask, abort, request
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

@app.route("/api/catalog", methods=["Post"])
def save_product():
    product = request.get_json() # read the payload as a dictionary from json string 

    # validate 
    # title and longer than 5 chars
    if not "title" in product or len(product["title"]) < 5:
        return abort(400, "There should be title. Title should be atr least 5 char longs")
    
    # should have a price
    if not "price" in product:
        return abort(400, "Price is required")

    # if the price is not and int and not a float, error 
    if not isinstance(product["price"], int) or isinstance(product["price"], float):
        return abort(400, "It is not a price")

    # the price should be greater than zero 
    if product["price"] < 0: 
        return abort(400, "Can not be less that zero")
    
    product["_id"] = random.randint(1000,5000) 
    catalog.append(product)
    return json.dumps(product) 

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

# get /api/categories
# return a list of strings, representing the UNIQUE categories 

@app.route("/api/categories")
def get_categories():

    res = []
    # 2 - print each category 
    for prod in catalog:
       category = prod["category"]
       if not category in res:
        res.append(category)


@app.route("/api/catalog/<category>")
def get_allproducts(category):
    res=[]
    for prod in catalog:
        if prod["category"] == category:
            res.append(prod)
            #append prod to the list
    return json.dumps(res)

coupons = []
#API Methods for Coupon Code
#code: Nick 
# get all get /api/coupons 
#save new  post /api/coupons
#get by code get /api/coupons/<code>

@app.route("/api/coupons")
def get_coupons():
    return json.dumps(coupons)

@app.route("/api/coupons", methods=["Post"])
def save_coupons():
    coupons = request.get_json()

    # validation


    coupons["_id"] = random.randint(500,900)
    coupons.append(coupons)
    return json.dumps(coupons)

@app.route("/api/coupon/<id>")
def get_couponsbycode(code):
    for coupon in coupons:
        if coupons["code"] == code:
            return json.dumps(coupon)
    return abort(404) # 400 not found

#start the server 
app.run(debug=True)