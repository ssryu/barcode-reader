from camera_client import CameraClient
from http_server import HttpServer
from web_socket_server import WebSocketServer

# line notify を利用する場合
LINE_NOTIFY_ACCESS_TOKEN = None


def main():
    http_server = HttpServer()
    http_server.start()

    web_socket_server = WebSocketServer(
        line_notify_access_token=LINE_NOTIFY_ACCESS_TOKEN
    )
    web_socket_server.start()

    # UI interaction は main thread で利用する必要があるので、
    # サーバをバックグランドで実行してカメラを main thread で実行する。
    # ref: https://github.com/opencv/opencv/issues/22602
    camera_client = CameraClient()
    camera_client.run_capture()


if __name__ == "__main__":
    main()
