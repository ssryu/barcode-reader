from camera_client import CameraClient
from http_server import HttpServer
from web_socket_server import WebSocketServer

http_server = HttpServer()
http_server.start()

web_socket_server = WebSocketServer()
web_socket_server.start()

# UI interaction は main thread で利用する必要があるので、
# サーバをバックグランドで実行してカメラを main thread で実行する。
# ref: https://github.com/opencv/opencv/issues/22602
camera_client = CameraClient()
camera_client.run_capture()
