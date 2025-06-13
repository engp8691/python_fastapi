import sys
import grpc
from app.grpc.chat_room.generated import chat_pb2
from app.grpc.chat_room.generated import chat_pb2_grpc
import time

def send_messages(username, stub):
    def generate():
        while True:
            msg = input(f"{username}> ")
            yield chat_pb2.ChatMessage(
                sender=username,
                message=msg,
                timestamp=int(time.time())
            )
    responses = stub.ChatStream(generate())
    for res in responses: # Blocking generator, server does this: `yield msg`
        print(f"[{res.timestamp}] {res.sender}: {res.message}")

def main():
    args = sys.argv[1:]
    username = "Client"
    if args:
        username = args[0]

    channel = grpc.insecure_channel('localhost:50051')
    stub = chat_pb2_grpc.ChatServiceStub(channel)
    send_messages(username, stub)

if __name__ == '__main__':
    main()
