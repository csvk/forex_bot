my_list = ["fred", "lentils", "bread", "apple", "pen"]

for item in my_list:
    if item == "pen":
        break
    if item == "lentils":
        continue
    print(item)

ans = 1

#while ans > 0:
#    print(ans)
#    ans -= 1

#for index in range(0,13,2):
#    print("range", index)

my_duck = {
    'age': 12,
    'name': 'Fred',
    'children': ['tigger', 'piglet'],
    'address': {
        'street': 'Baker',
        'plz': 54687
    }
}

for key in my_duck.keys():
    print(key)