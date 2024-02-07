import json

my_duck = {
    'age': 12,
    'children': ['possum', 'piglet']
}

my_list = [my_duck, my_duck]

#print(my_duck)
print(my_list)

duck_json = json.dumps(my_list, indent=2)
print(duck_json)

ob = json.loads(duck_json)
print(ob)
print(type(ob[0]))

