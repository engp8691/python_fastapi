import grpc
import asyncio

# -- Greeter Import (async) --
from app.grpc import greeter_pb2_grpc, greeter_pb2

# -- Ecommerce Imports (async) --
from app.grpc.ecommerce.generated import (
    common_pb2,
    user_pb2,
    user_pb2_grpc,
    product_pb2,
    product_pb2_grpc,
    order_pb2,
    order_pb2_grpc,
    inventory_pb2,
    inventory_pb2_grpc,
    payment_pb2,
    payment_pb2_grpc,
)
from app.grpc.ecommerce.generated import inventory_pb2

# -- Greeter Service --
class Greeter(greeter_pb2_grpc.GreeterServicer):
    async def SayHello(self, request, context):
        return greeter_pb2.HelloReply(message=f"Hello, {request.name}!")

# Mock data
mock_product = common_pb2.Product(
    id="p1", name="Laptop", price=1299.99, category="Electronics"
)
mock_user = common_pb2.User(
    id="u123", name="Alice Example", email="alice@example.com")


# --- Service Implementations ---
class UserService(user_pb2_grpc.UserServiceServicer):
  async def GetUser(self, request, context):
    return common_pb2.User(
        id=request.user_id, name=mock_user.name, email=mock_user.email
    )

  async def CreateUser(self, request, context):
    new_user = common_pb2.User(
        id="new-id", name=request.name, email=request.email)
    print("User created:", new_user)
    return new_user


class ProductService(product_pb2_grpc.ProductServiceServicer):
  async def GetProduct(self, request, context):
    return common_pb2.Product(
        id=request.product_id,
        name=mock_product.name,
        price=mock_product.price,
        category=mock_product.category,
    )

  async def ListProducts(self, request, context):
    return product_pb2_grpc.ListProductsResponse(
        products=[
            mock_product,
            common_pb2.Product(
                id="p2", name="Phone", price=799.99, category="Electronics"
            ),
        ]
    )


class InventoryService(inventory_pb2_grpc.InventoryServiceServicer):
  async def CheckInventory(self, request, context):
    items = [
        common_pb2.InventoryItem(product_id=id, quantity=100)
        for id in request.product_ids
    ]
    return inventory_pb2.CheckInventoryResponse(items=items)

  async def UpdateInventory(self, request, context):
    for update in request.updates:
      print(f"Inventory updated for {update.product_id}: {update.delta}")
    return inventory_pb2.UpdateInventoryResponse(success=True)


class PaymentService(payment_pb2_grpc.PaymentServiceServicer):
  async def ProcessPayment(self, request, context):
    print(
        f"Processing payment for {request.user_id}, amount: {request.amount}")
    return payment_pb2.ProcessPaymentResponse(
        success=True, transaction_id="txn-98765"
    )


class OrderService(order_pb2_grpc.OrderServiceServicer):
  def __init__(self):
    self.user_stub = user_pb2_grpc.UserServiceStub(
        grpc.aio.insecure_channel("localhost:50051")
    )
    self.inventory_stub = inventory_pb2_grpc.InventoryServiceStub(
        grpc.aio.insecure_channel("localhost:50051")
    )
    self.payment_stub = payment_pb2_grpc.PaymentServiceStub(
        grpc.aio.insecure_channel("localhost:50051")
    )

  async def CreateOrder(self, request, context):
    print(f"Creating order for user {request.user_id}")
    user_resp = await self.user_stub.GetUser(user_pb2.GetUserRequest(user_id="u1"))
    # Step 1: Check User
    if user_resp.id != "u1":
      context.set_code(grpc.StatusCode.PERMISSION_DENIED)
      context.set_details("Unauthorized user")
      return common_pb2.Order()

    # Step 2: Check Inventory
    inv_resp = await self.inventory_stub.CheckInventory(
        inventory_pb2.CheckInventoryRequest(
            product_ids=request.product_ids)
    )
    if any(item.quantity < 1 for item in inv_resp.items):
      context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
      context.set_details("Some products are out of stock")
      return common_pb2.Order()

    # Step 3: Process Payment
    pay_resp = await self.payment_stub.ProcessPayment(
        payment_pb2.ProcessPaymentRequest(
            user_id=request.user_id,
            order_id="order-id-123",
            amount=2599.98,
        )
    )
    if not pay_resp.success:
      context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
      context.set_details("Payment failed")
      return common_pb2.Order()

    # Step 4: Create Order
    order = common_pb2.Order(
        id="order-id-123",
        user_id=request.user_id,
        product_ids=request.product_ids,
        total_price=2599.98,
        status="PENDING",
    )

    # Step 5: Update Inventory
    await self.inventory_stub.UpdateInventory(
        inventory_pb2.UpdateInventoryRequest(
            updates=[
                inventory_pb2.InventoryUpdate(product_id=id, delta=-1)
                for id in request.product_ids
            ]
        )
    )

    return order

  async def GetOrder(self, request, context):
    return common_pb2.Order(
        id=request.order_id,
        user_id="u123",
        product_ids=["p1", "p2"],
        total_price=2599.98,
        status="PENDING",
    )


async def start_grpc_server():
  server = grpc.aio.server()

  greeter_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
  user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
  product_pb2_grpc.add_ProductServiceServicer_to_server(
      ProductService(), server)
  inventory_pb2_grpc.add_InventoryServiceServicer_to_server(
      InventoryService(), server
  )
  payment_pb2_grpc.add_PaymentServiceServicer_to_server(
      PaymentService(), server)
  order_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)

  server.add_insecure_port("[::]:50051")
  await server.start()
  print("✅ gRPC server running on port 50051")
  await server.wait_for_termination()


if __name__ == "__main__":
  asyncio.run(start_grpc_server())
