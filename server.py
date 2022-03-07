
from random import random
from sqlite3 import Cursor
from mock_data import catalog
from flask import Flask, abort, request
from about_me import me 
import json 
from flask_cors import CORS
from config import db
from bson import ObjectId

#create the server/app
app = Flask("server")
CORS(app)

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

    cursor = db.products.find({})
    results = []
    for prod in cursor:
        results.append(prod)
        prod["_id"] = str(prod["_id"])
     

    return json.dumps(results)
    

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
    if not isinstance(product["price"], int) and not isinstance(product["price"], float):
        return abort(400, "It is not a price")

    # the price should be greater than zero 
    if product["price"] < 0: 
        return abort(400, "Can not be less that zero")
    
    db.products.insert_one(product)


    #hack to fix the _id 
    product["_id"] = str(product["_id"])
    return json.dumps(product) 

#get /api/catalog/count
@app.route("/api/catalog/count")
def get_catalogcount():  
    cursor = db.products.find({})   
    count = len(cursor)
    for prod in cursor:
        count += 1
    return json.dumps(cursor.count())

@app.route("/api/catalog/sum")
def get_sum():
    total = 0
    for prod in catalog:
        total += prod["price"]

    res = "$" + str(total)
    return json.dumps(res)

@app.route("/api/product/<id>")
def get_product(id):
    prod = db.products.find_one({"_id": ObjectId(id)})
    if not ObjectId.is_valid(id):
        return abort(400, "id is not a valid ObjectId")
    if not prod:
        return abort(404, "Product not found")

    prod["_id"] = str(prod["_id"])
    return json.dumps(prod)
    
    #return abort(404)  # 400 not found

@app.route("/api/product/most_expensive")
def get_most_expensive():
    pivot = catalog[0]
    cursor = db.products.find({})
    for prod in cursor:
        if prod["price"] > pivot["price"]:
            pivot = prod


        pivot["_id"] = str(pivot["_id"])
    return json.dumps(pivot)

# get /api/categories
# return a list of strings, representing the UNIQUE categories 

@app.route("/api/categories")
def get_categories():

    res = []
    cursor = db.products.find({})
    # 2 - print each category 
    for prod in cursor:
       category = prod["category"]
       if not category in res:
        res.append(category)
    return json.dumps(res)


@app.route("/api/catalog/<category>")
def get_allproducts(category):
    res=[]
    cursor = db.products.find({"category": category})
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        res.append(prod)

    return json.dumps(res)

coupons = []
#API Methods for Coupon Code
#code: Nick 
# get all get /api/coupons 
#save new  post /api/coupons
#get by code get /api/coupons/<code>

@app.route("/api/coupons")
def get_coupons():
    cursor = db.discounts.find({})
    results = []
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
    return json.dumps(results)

@app.route("/api/coupons", methods=["Post"])
def save_coupons():
    coupon = request.get_json()

    db.coupons.insert_one(coupon)

    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)

@app.route("/api/coupon/<id>")
def get_couponsbycode(code):
    coupon = db.products.find({"code": code})
    if not coupon:
        return abort(404, 'Coupon not found for code: ' + code)
    coupon["_id"] = str(coupon['_id'])
    return json.dumps(coupon)
    

@app.route("/api/saveOrders", methods = ["Post"])
def save_orders():
    order = request.get_json()

    db.orders.insert_one(order)

    order["_id"] = str(order["_id"])
    return json.dumps(order)


@app.route("/api/retrieveOrders")
def get_orders():
    cursor = db.orders.find({})
    results = []
    for order in cursor:
        order["_id"] = str(order["_id"])
    return json.dumps(results)


@app.route("/api/retrieveOrders/<user_id>")
def get_ordersbyId(user_id):
    order = db.orders.find_one({"user_id": user_id})
    if not order:
        return abort(404, "Not correct ID")
    order["_id"] = str(order['_id'])
    return json.dumps(order)

#start the server 
app.run(debug=True)