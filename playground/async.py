import asyncio
import math
import random

async def simulateFetchUser(name, seconds):
    await asyncio.sleep(seconds)

    return f"User {name}"

async def simulateFetchOrdersOfUser(user):
    orders = ['Order A', 'Order B', 'Order C', 'Order D']
    orderNumber = random.randint(0, 3)
    await asyncio.sleep(orderNumber)

    return f'{user} made {orders[orderNumber]}'

async def main():
    user = await simulateFetchUser('Me', 1)
    theOrder = await simulateFetchOrdersOfUser(user)
    print(theOrder)

    try:
        users = await asyncio.gather(
            simulateFetchUser("A", 1),
            simulateFetchUser("B", 2),
            simulateFetchUser("C", 3)
        )
        print("Fetched users:", users)

        fetchOrderTasks = [simulateFetchOrdersOfUser(user) for user in users]
        orders = await asyncio.gather(*fetchOrderTasks)
        print("Fetched orders:", orders)
    except Exception as e:
        print("Error:", e)


# asyncio.run(main())

user = {"name": "yonglin", "zipcode": 30, "city": "Boston", "address": "270 main street"}

def safe_get(obj, *attrs):
    for attr in attrs:
        obj = getattr(obj, attr, None)
        if obj is None:
            return None
    return obj

obj = safe_get(user, "address", "city", "zipcode")

print(999949, obj)


def example(*args, **kwargs):
    print(args)
    print(kwargs)

example(1, 2, a=3, b=4)


def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1
        print(9999964, i)

gen1 = count_up_to(10)
gen2 = count_up_to(12)
print(66666, next(gen1))
print('A gap in between')
print(66667, next(gen1))
# print(66668, next(gen1))
# print(66669, next(gen1))
# print(66670, next(gen2))


def decorator(func):
    def wrapper():
        print("Before function")
        func()
        print("After function")
    return wrapper

@decorator
def greet():
    print("Hello!")

greet()



def area(*args):
    if len(args) == 1:
        # Circle: π * r^2
        radius = args[0]
        return math.pi * radius ** 2
    elif len(args) == 2:
        # Rectangle: length * width
        length, width = args
        return length * width
    elif len(args) == 3:
        # Triangle using Heron's formula
        a, b, c = args
        s = (a + b + c) / 2
        return math.sqrt(s * (s - a) * (s - b) * (s - c))
    else:
        raise ValueError("Unsupported number of arguments")
    
print(area(3))
print(area(3, 4))
print(area(3, 4, 5))