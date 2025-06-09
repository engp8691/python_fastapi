import grpc
from app.grpc.ecommerce.generated import product_pb2, product_pb2_grpc


def run():
  channel = grpc.insecure_channel("localhost:50051")
  stub = product_pb2_grpc.ProductServiceStub(channel)
  request = product_pb2.GetProductRequest(product_id="12345")
  response = stub.GetProduct(request)
  print(
      f"Product received: ID={response.id}, Name={response.name}, Price={response.price}"
  )


if __name__ == "__main__":
  run()
