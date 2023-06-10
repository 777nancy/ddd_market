from marketanalysis.domain.repository.interface import (
    AbstractSlackNotificationRepository,
)
from marketanalysis.domain.slack_message import SlackMessage
from marketanalysis.platform.slack import Slack
from marketanalysis.settings.constants import CHANNEL_ID, SLACK_FILE_URL, TOKEN


class SlackNotificationRepository(AbstractSlackNotificationRepository):
    def __init__(self, slack: Slack | None = None) -> None:
        self.slack = slack or Slack(TOKEN, CHANNEL_ID, SLACK_FILE_URL)

    def notify(self, message: SlackMessage, file_uploads_data: list[dict] | None = None):
        return self.slack.notify(message.format(), file_uploads_data)
