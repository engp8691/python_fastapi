# app/routes/rpc.py
import grpc
from fastapi import APIRouter
from app.grpc import greeter_pb2, greeter_pb2_grpc

router = APIRouter()

def get_greeting(name: str = "Yonglin") -> str:
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = greeter_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(greeter_pb2.HelloRequest(name=name))
        return response.message

@router.get("/rpc/greeting")
def rpc_greeting(name: str = "Yonglin"):
    return {"message": get_greeting(name)}
