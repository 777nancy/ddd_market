import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackClientError


class Slack(object):
    def __init__(self, token, channel_id, slack_file_post_url) -> None:
        self.token = token
        self.channel_id = channel_id
        self.slack_file_post_url = slack_file_post_url

    def _notify_with_file(self, message, file_path):
        files = {"file": open(file_path, "rb")}

        param = {
            "token": self.token,
            "channels": self.channel_id,
            "filename": "filename",
            "initial_comment": message,
            "title": "title",
        }

        requests.post(url=self.slack_file_post_url, params=param, files=files)

    def _notify_with_data(self, message, file_uploads_data: list[dict]):
        client = WebClient(token=self.token)
        client.files_upload_v2(
            file_uploads=file_uploads_data,
            channel=self.channel_id,
            initial_comment=message,
        )

    def _notify_simply(self, message):
        client = WebClient(token=self.token)
        response = client.chat_postMessage(channel=self.channel_id, text=message)

        print(response.status_code)
        if response.status_code != 200:
            raise SlackClientError

    def notify(self, message: str, file_uploads_data: list[dict] | None = None):
        if file_uploads_data:
            self._notify_with_data(message, file_uploads_data)
        else:
            self._notify_simply(message)
