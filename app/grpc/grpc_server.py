import grpc
import asyncio

# -- Greeter Import (async) --
from app.grpc import greeter_pb2_grpc, greeter_pb2

# -- Ecommerce Imports (async) --
from app.grpc.ecommerce.generated import (
    user_pb2_grpc,
    product_pb2_grpc,
    order_pb2_grpc,
    common_pb2,
)

# -- Greeter Service --
class Greeter(greeter_pb2_grpc.GreeterServicer):
    async def SayHello(self, request, context):
        return greeter_pb2.HelloReply(message=f"Hello, {request.name}!")

# -- User Service --
class UserService(user_pb2_grpc.UserServiceServicer):
    async def GetUser(self, request, context):
        return common_pb2.User(id=request.user_id, name="Alice", email="alice@example.com")

# -- Product Service --
class ProductService(product_pb2_grpc.ProductServiceServicer):
    async def GetProduct(self, request, context):
        return common_pb2.Product(id=request.product_id, name="MacBook Pro", price=1999.99)

# -- Order Service --
class OrderService(order_pb2_grpc.OrderServiceServicer):
    async def GetOrder(self, request, context):
        user = common_pb2.User(id="u1", name="Alice", email="alice@example.com")
        product = common_pb2.Product(id="p1", name="MacBook Pro", price=1999.99)
        item = common_pb2.OrderItem(product=product, quantity=1)
        return common_pb2.Order(
            id=request.order_id,
            user=user,
            items=[item],
            total_price=1999.99
        )

async def start_grpc_server():
    server = grpc.aio.server()

    greeter_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    product_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
    order_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)

    server.add_insecure_port("[::]:50051")
    await server.start()
    print("✅ gRPC server running on port 50051")
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(start_grpc_server())
