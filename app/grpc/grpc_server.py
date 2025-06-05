import grpc
from app.grpc import greeter_pb2_grpc, greeter_pb2

class Greeter(greeter_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return greeter_pb2.HelloReply(message=f"Hello, {request.name}!")

async def start_grpc_server():
    server = grpc.aio.server()
    greeter_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    print("✅ gRPC server is running on port 50051")
    await server.wait_for_termination()
