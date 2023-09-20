from prediction import logger
from prediction.config.configuration import ConfigManager
from slack_sdk import WebClient
import os

class SlackSender:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager
        self.enabled = config_manager.config.slack.enabled
        self.channel_id = config_manager.config.slack.channel_id
        if self.enabled:
            self.client = WebClient(token=os.environ['SLACK_API_TOKEN'])

    def send(self, json_gen):
        if not self.enabled:
            logger('Slack sending is NOT enabled')
            return
        for message in json_gen:
            # Send the message
            format_message = f'Summary for the last meeting:\n{message}'
            try:
                response = self.client.chat_postMessage(channel=self.channel_id, text=format_message)
                if response['ok']:
                    logger.info(f'Successfully send summary to Slack channel {self.channel_id}!')
                else:
                    logger.info(f'Sending to Slack channel {self.channel_id} failed, {response}')
            except Exception as e:
                logger.error(f'Error sending message to Slack channel {self.channel_id}, {e}')