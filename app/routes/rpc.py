# app/routes/rpc.py
import grpc
from google.protobuf.json_format import MessageToDict
from fastapi import APIRouter
from app.grpc import greeter_pb2, greeter_pb2_grpc
from app.grpc.ecommerce.generated import product_pb2, product_pb2_grpc
from app.grpc.ecommerce.generated import order_pb2, order_pb2_grpc
from app.grpc.ecommerce.generated import user_pb2, user_pb2_grpc

router = APIRouter()

def get_greeting(name: str = "Yonglin") -> str:
    with grpc.insecure_channel("localhost:50051") as channel:
        result = {
            'desc': "This route is calling all the gRPC services of 'greeting', 'order', 'product' and 'user'. It then returns all responses from the services.",
            'note': "Read the README.MD file for the details"
        }

        stub = greeter_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(greeter_pb2.HelloRequest(name=name))
        result["greeting"] = response.message

        stub = product_pb2_grpc.ProductServiceStub(channel)
        request = product_pb2.GetProductRequest(product_id='12345')
        response = stub.GetProduct(request)
        result["product"] = f"Product received: ID={response.id}, Name={response.name}, Price={response.price}"

        stub = order_pb2_grpc.OrderServiceStub(channel)
        request = order_pb2.GetOrderRequest(order_id="o1")
        response = stub.GetOrder(request)
        order_dict = MessageToDict(response)
        result["order"] = order_dict

        stub = user_pb2_grpc.UserServiceStub(channel)
        request = user_pb2.GetUserRequest(user_id="u1")
        response = stub.GetUser(request)
        user_dict = MessageToDict(response)
        result["user"] = user_dict

        print(result)

        return result

@router.get("/rpc/greeting")
def rpc_greeting(name: str = "Yonglin"):
    return get_greeting(name)
