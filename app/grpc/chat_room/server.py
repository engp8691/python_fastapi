import grpc
from concurrent import futures
import threading
import queue

from app.grpc.chat_room.generated import chat_pb2
from app.grpc.chat_room.generated import chat_pb2_grpc

client_queues = []

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def ChatStream(self, request_iterator, context):
        q = queue.Queue()
        client_queues.append(q)
        print("New client connected")

        def read_incoming():
            try:
                for msg in request_iterator: # Blocking generator, the client does this: yield chat_pb2.ChatMessage(...)
                    print(f"[{msg.timestamp}] {msg.sender}: {msg.message}")
                    for client_q in client_queues:
                        if client_q != q:
                            client_q.put(msg)
            except Exception as e:
                print("Client disconnected", e)
            finally:
                print("Removing client queue")
                client_queues.remove(q)

        threading.Thread(target=read_incoming, daemon=True).start()

        while True:
            try:
                msg = q.get(timeout=60)
                yield msg
            except queue.Empty:
                continue

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()