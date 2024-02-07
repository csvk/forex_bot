my_list = [34, 56, 98, 12, 54, 34]

print(my_list)

# list comprehension
new_list = [ f"{x}_V" for x in my_list]
print(new_list)

new_list = [ x for x in my_list if x > 50]
print(new_list)

new_list = [ "Good" if x > 50 else "Bad" for x in my_list ]
print(new_list)

[print(f"K{x}") for x in my_list]

# dict comprehension
my_duck = {
    'age': 12,
    'name': 'Fred',
    'duckings': 3,
    'temp': 48.0
}
new_ob = { k: v for k, v in my_duck.items() }
print(new_ob)

new_ob = { v: k for k, v in my_duck.items() }
print(new_ob)

new_ob = { x: f"X{x}" for x in my_list }
print(new_ob)

[print(k, v) for k, v in my_duck.items()]












