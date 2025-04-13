import asyncio
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


asyncio.run(main())


