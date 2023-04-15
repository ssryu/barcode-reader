import requests


class LineNotifier:
    LINE_API_URL = "https://notify-api.line.me/api/notify"

    def __init__(self, access_token: str):
        self.line_api_token = access_token

    def notify(self, msg):
        param = {"message": msg}
        header = {"Authorization": "Bearer " + self.line_api_token}
        requests.post(self.LINE_API_URL, params=param, headers=header)
