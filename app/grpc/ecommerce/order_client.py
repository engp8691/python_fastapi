import grpc
from app.grpc.ecommerce.generated import order_pb2, order_pb2_grpc

def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = order_pb2_grpc.OrderServiceStub(channel)

    request = order_pb2.GetOrderRequest(order_id="o1")
    response = stub.GetOrder(request)

    print("Order Response:")
    print(response)

if __name__ == "__main__":
    run()
