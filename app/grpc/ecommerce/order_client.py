import grpc
from app.grpc.ecommerce.generated import order_pb2, order_pb2_grpc


def run():
  channel = grpc.insecure_channel("localhost:50051")
  stub = order_pb2_grpc.OrderServiceStub(channel)

  # CreateOrder call
  create_request = order_pb2.CreateOrderRequest(
      user_id="user-123", product_ids=["p1", "p2"]
  )
  order = stub.CreateOrder(create_request)
  print("Created Order:", order)

  # GetOrder call
  get_request = order_pb2.GetOrderRequest(order_id=order.id)
  fetched_order = stub.GetOrder(get_request)
  print("Fetched Order:", fetched_order)


if __name__ == "__main__":
  run()
