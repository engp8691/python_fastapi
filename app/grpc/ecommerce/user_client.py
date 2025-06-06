import grpc
from app.grpc.ecommerce.generated import user_pb2, user_pb2_grpc

def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = user_pb2_grpc.UserServiceStub(channel)

    request = user_pb2.GetUserRequest(user_id="u1")
    response = stub.GetUser(request)

    print("User Response:")
    print(response)

if __name__ == "__main__":
    run()
