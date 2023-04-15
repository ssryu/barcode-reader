import threading
import webbrowser
from time import sleep

import cv2
from pyzbar.pyzbar import decode
from websocket import WebSocketApp

from database_manager import DatabaseManager


# TODO: サーバから在庫更新結果を受け取り、音を鳴らす機能?
class CameraClient:
    def __init__(
        self,
        window_name="JAN CODE READER",
        http_server_url="localhost",
        http_server_port=8080,
        socket_server_url="localhost",
        socket_server_port=8081,
    ):
        self.window_name = window_name
        self.can_scan = True

        self.web_socket_app = WebSocketApp(
            url=f"ws://{socket_server_url}:{socket_server_port}"
        )
        threading.Thread(target=self.web_socket_app.run_forever).start()
        webbrowser.open(f"http://{http_server_url}:{http_server_port}")

    def run_capture(self):
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)

        while capture.isOpened():
            is_read, frame = capture.read()

            cv2.imshow(self.window_name, frame)
            cv2.waitKey(1)

            if not cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE):
                break

            # frame が読み取れていない場合
            if not is_read:
                continue

            if self.can_scan is False:
                continue

            barcodes = decode(frame)
            for i, barcode in enumerate(barcodes):
                code = barcode.data.decode("utf-8")
                if self.is_jan(code):
                    self.can_scan = False
                    self.web_socket_app.send(code)
                if i == len(barcodes) - 1:
                    # 複数の barcode を最後まで読み取り終えたら、しばらく scan できないようにする。
                    threading.Thread(target=self.scan_wait).start()

        # self.db = DatabaseManager()
        # self.db.export_excel()
        # self.db.close()
        capture.release()
        self.web_socket_app.close()

    def is_jan(self, code):
        return (len(code) == 13 or len(code) == 8) and (
            code[:2] == "49" or code[:2] == "45"
        )

    def scan_wait(self):
        sleep(2)
        self.can_scan = True
