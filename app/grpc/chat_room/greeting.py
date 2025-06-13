import sys
import grpc
import time
from app.grpc.chat_room.generated import chat_pb2
from app.grpc.chat_room.generated import chat_pb2_grpc

def send_messages(username, default_msg, stub):
    def generate():
        while True:
            try:
                msg = input(f"{username}> ").strip() 
                if not msg:
                    msg = default_msg
                yield chat_pb2.ChatMessage(
                    sender=username,
                    message=msg,
                    timestamp=int(time.time())
                )
            except EOFError:
                break

    try:
        responses = stub.ChatStream(generate())
        for res in responses: # Blocking generator, server does this: `yield msg`
            print(f"[{res.timestamp}] {res.sender}: {res.message}")
    except grpc.RpcError as e:
        print("Disconnected from server:", e.details())
        raise e

def create_channel():
    return grpc.insecure_channel('localhost:50051')

def main():
    args = sys.argv[1:]
    username = args[0] if args else "Client"
    default_msg = args[1] if len(args) > 1 else f"Default message of {username}"

    backoff = 1
    max_backoff = 10

    while True:
        print(f"Retrying in {backoff} seconds...")
        try:
            channel = create_channel()
            stub = chat_pb2_grpc.ChatServiceStub(channel)
            backoff = 1
            send_messages(username, default_msg, stub)
        except grpc.RpcError:
            print(f"Retrying in {backoff} seconds...")
            time.sleep(backoff)
            backoff = min(backoff + 1, max_backoff)
        except KeyboardInterrupt:
            print("Client exiting...")
            break

if __name__ == '__main__':
    main()
