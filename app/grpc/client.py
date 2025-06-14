import grpc
from app.grpc import greeter_pb2, greeter_pb2_grpc


def run():
  with grpc.insecure_channel("localhost:50051") as channel:
    stub = greeter_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(greeter_pb2.HelloRequest(name="Yonglin"))
    print("Greeter client received: " + response.message)


if __name__ == "__main__":
  run()
