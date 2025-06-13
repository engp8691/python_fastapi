# python_fastapi

## Python fast API

### Steps to check

**_NOTE:_**
My codes tested on my local machine under Python 3.13.2
The backend Database is PostgreSQL of postgres:latest in Docker
the .env file is changed to env.sample file. Change the values according to your DB.
Follow the following steps and run the script to create the DB and tables.

- Step 1: `python -m venv venv`
- step 2: `source venv/bin/activate`
- Step 3: go inside the `fastapi_python` folder and install all the packages required with command of `pip install -r requirements.txt`
- Step 4: initiate the database by `python -m app.db.create_tables`
- Step 5: run the server by `uvicorn app.main:app --reload`
- Step 6: run unit tests by `pytest --cov=app --cov-report=html`
- Step 7: check the coverate under `htmlcov/index.html`
- Step 8: swagger docs under `http://localhost:8000/docs`
- Step 9: backup your package requirements by `pip freeze > requirements.txt`

### steps to add gRPC inside

- 1: create the grpc folder under app
- 2: create the greeter.proto file under the grpc folder
- 3: at the root folder of `fastapi_python` run

`python -m grpc_tools.protoc -I./app/grpc --python_out=./app/grpc --grpc_python_out=./app/grpc app/grpc/greeter.proto`

- 4: at the root folder of `fastapi_python` run

`python -m grpc_tools.protoc -Iapp/grpc/ecommerce/protos --python_out=app/grpc/ecommerce/generated --grpc_python_out=app/grpc/ecommerce/generated app/grpc/ecommerce/protos/common.proto app/grpc/ecommerce/protos/user.proto app/grpc/ecommerce/protos/order.proto app/grpc/ecommerce/protos/product.proto`

- 5: at the root folder of `fastapi_python` run

`find app/grpc/ecommerce/generated -type f -name "*.py" -exec sed -i '' -E 's/^import (.*_pb2)/from . import \1/' {} \;`

**_NOTE:_** step 5 manually fixes the relative path importing issue. TODO: Do research on this.

- 6: modidy `main.py` to call `start_grpc_server`
- 7: start the app by `uvicorn app.main:app --reload`
- 8: run the client to invoke the RPC by running `python -m app.grpc.client`

### Lets make the client call inside a REST API

- 1: add the route of `fastapi_python/app/routes/rpc.py`
- 2: start python REST API app
- 3: access it in the browser as `http://127.0.0.1:8000/rpc/greeting?name=YonglinLee`

### Test the server and the clients
<!--
python -m grpc_tools.protoc -Iapp/grpc/ecommerce/protos --python_out=app/grpc/ecommerce/generated --grpc_python_out=app/grpc/ecommerce/generated app/grpc/ecommerce/protos/common.proto app/grpc/ecommerce/protos/user.proto app/grpc/ecommerce/protos/order.proto app/grpc/ecommerce/protos/product.proto

find app/grpc/ecommerce/generated -type f -name "*.py" -exec sed -i '' -E 's/^import (.*_pb2)/from . import \1/' {} \;
-->

**_NOTE:_** After step 7 starts fastapi app, test all the clients. If step 7 is not started, start the server

`python -m app.grpc.grpc_server`

test all the clients:

**_NOTE:_** Make sure it is in the folder of `./fastapi_python`

- 1: python -m app.grpc.client
- 2: python -m app.grpc.ecommerce.order_client
- 3: python -m app.grpc.ecommerce.product_client
- 4: python -m app.grpc.ecommerce.user_client

## Chat room

### At the root folder of `fastapi_python` run

```sh
python -m grpc_tools.protoc -Iapp/grpc/chat_room/protos --python_out=app/grpc/chat_room/generated --grpc_python_out=app/grpc/chat_room/generated app/grpc/chat_room/protos/chat.proto
```

```sh
find app/grpc/chat_room/generated -type f -name "*.py" -exec sed -i '' -E 's/^import (.*_pb2)/from . import \1/' {} \;
```

```sh
python -m app.grpc.chat_room.server
```

```sh
python -m app.grpc.chat_room.greeting Yonglin
python -m app.grpc.chat_room.greeting Alice
```
