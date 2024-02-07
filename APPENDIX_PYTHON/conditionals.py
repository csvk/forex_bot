x,y,z = 20,30,40
my_list = ["fred", "roger", "mick"]

# > >= < <= ==, or and (in)
if x == 20:
    print("Yes")
    print("Yes2")
    if y < 30:
        print("Y is also")
        print("Y is also2")

ans = 'fred'
if ans in my_list:
    print("Fred")

sentence = "Lazy fox jumped"
if 'fox' in sentence:
    print("Hello fox")

if x == 19:
    print("uhoh")
elif z > 40:
    print("z is here")
else:
    print("failed else")

if x == 21 or z == 40:
    print("here they are")

duck = {
    'age': 12,
    'name': 'Fred'
}

if 'age' in duck.keys():
    print("TRUE")