import threading

from websocket_server import WebsocketServer

from database_manager import DatabaseManager


class WebSocketServer:
    def __init__(
        self,
        host="localhost",
        port=8081,
    ):
        self.web_socket_server = WebsocketServer(host=host, port=port)
        self.web_socket_server.set_fn_new_client(self.new_client)
        self.web_socket_server.set_fn_message_received(self.message_received)

        self.db = DatabaseManager()

    def start(self):
        threading.Thread(target=self.web_socket_server.run_forever).start()

    def shutdown(self):
        self.web_socket_server.shutdown()

    def new_client(self, client, server):
        print(f"Hello! client: {client}, server: {server}")

    def message_received(self, client, server, message: str):
        """
        Args:
            message(str):
                from camera client: "{jancode}" 形式の文字列
                    このメッセージが届いたら、
                    mode を追加するために javascript client 側にメッセージを転送する。
                from javascript client: "{mode} {jancode}" 形式の文字列
                    mode(str): in|out
                    このメッセージが届いたら、在庫を更新する。
        """
        splited_message = message.split()
        if len(splited_message) == 1:
            self.web_socket_server.send_message_to_all(message)
            return

        mode = splited_message[0]
        jancode = splited_message[1]

        if mode == "in":
            self.db.update_stock(jancode, 1)
        elif mode == "out":
            self.db.update_stock(jancode, -1)
            # alert = self.db.check_alert(code)
            # if alert is not None:
            #     self.line_notify(alert['product_name'] + 'がなくなるぞ！')
