from ast import Num


def print_name():
    print("Nick Lucien")

print_name()

def test_dict():
    print("Dictionary")

me = {
    "first" : "Nick",
    "last": "Lucien",
    "age": 35,
    "hobbies": "[]",
    "address": {
        "street": "evergreen",
        "city": "springsfield",

    }
    
    

}

address = me("address")
print(address["street"] + "" + address["city"])

def younger_person(): 
    ages =  [12,42,32,50,56,14,78,30,51,89,12,38,67,10]
    pivot = ages[0]
    for num in ages:
        if pivot < num :
            pivot = num 
    print("pivot")

print_name()
test_dict()
younger_person()
        









# funcrtion to print your name 
# call the function 
# run the script