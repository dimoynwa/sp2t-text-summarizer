from datasetcreation.config.configuration import ConfigManager
from datasetcreation import logger
import requests
from ensure import ensure_annotations
from datasetcreation.utils.common import get_slack_auth_token
import time

STAGE_NAME = "Fetch conversations"

class ConversationsStage:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager
        self.channel_ids = self.config_manager.config.slack.channels
        self.min_replies = self.config_manager.config.slack.min_replies
        self.limit = self.config_manager.config.slack.limit

    @ensure_annotations
    def main(self):
        auth_token = get_slack_auth_token()
        
        for chan in self.channel_ids:
            logger.info(f'Geting conversations for channels {chan}...')
            for ts in self._fetch_conversations(chan, auth_token):
                yield chan, ts

    def _fetch_conversations(self, channel_id: str, auth_token: str, count=0, cursor=None):
        url = self.config_manager.config.slack.conversations_url.replace('{channel_id}', channel_id)
        if cursor:
            url = url + f'&cursor={cursor}'
        headers = {'Authorization': f'Bearer {auth_token}'}
        logger.info(f'Calling {url}...')
        try:
            response = requests.get(url, headers=headers)
            response_body = response.json()
        except Exception as e:
            logger.error(f'Error calling url {url}, {e}')
            return
        for message in response_body['messages']:
            if 'reply_count' in message and message['reply_count'] >= self.min_replies:
                yield message['ts']
                count += 1
                if count % 10 == 0:
                    logger.info(f'Fetched {count} conversations.')
            if count >= self.limit:
                return
        time.sleep(1)
        if response_body['has_more']:
            new_cursor = response_body['response_metadata']['next_cursor']
            for ts in self._fetch_conversations(channel_id, auth_token, count=count, cursor=new_cursor):
                yield ts

if __name__ == '__main__':
    config_manager = ConfigManager()
    stage = ConversationsStage(config_manager)
    for channel, ts in stage.main():
        logger.info(f'Channel and ts: {channel}, {ts}')