from src.datasetcreation.config.configuration import ConfigManager
from ensure import ensure_annotations

from src.datasetcreation.pipeline.conversations_stage import ConversationsStage
from src.datasetcreation.pipeline.replies_stage import RepliesStage
from src.datasetcreation import logger

import re
from urllib.parse import urlparse

STAGE_NAME = 'Preprocess conversation'

class Preprocess:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager

    @ensure_annotations
    def main(self, thread_generator):
        for channel_id, ts, thread in thread_generator:
            conversation = '\n'.join([self._get_message_user(message) + ':' + self._clean_text(message['text']) for message in thread['messages']])
            conversation = self._clean_conversation(conversation)
            conversation = self._remove_empty_lines(conversation)
            yield channel_id, ts, conversation
            
    @ensure_annotations
    def _clean_text(self, text: str) -> str:
        cleaned_text = text.replace(r'\n', ' ')
        cleaned_text = cleaned_text.replace('`', '')
        cleaned_text = cleaned_text.replace("'", '')

        uuid_pattern = r'\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b'

        # Replace UUIDs with the specified replacement text
        cleaned_text = re.sub(uuid_pattern, '<UUID>', cleaned_text)

        url_pattern = r'https?://\S+'

        def replace_url(match):
            return '<URL>'

        # Replace URLs with their hostnames
        cleaned_text = re.sub(url_pattern, replace_url, cleaned_text)

        # Regular expression to match Cyrillic characters
        cyrillic_pattern = re.compile(r'[а-яА-ЯёЁ]')
        cleaned_text = re.sub(cyrillic_pattern, '', cleaned_text)

        return cleaned_text
    
    @ensure_annotations
    def _clean_conversation(self, conversation: str):
        # Remove lines starting with '\s{4,}at as those are stacktrace elements'
        clean_conversation = re.sub(r'^\n\s{4,}at.*?$', '', conversation, flags=re.MULTILINE)
        clean_conversation = re.sub(r'^\t+at.*?$', '', clean_conversation, flags=re.MULTILINE)
        return clean_conversation
    
    @ensure_annotations
    def _remove_empty_lines(self, conversation: str):
        # Split the text into lines, remove empty lines, and join the non-empty lines
        lines = [line for line in conversation.splitlines() if line.strip()]
        return '\n'.join(lines)

    def _get_message_user(self, message):
        user = 'NOT_ACTIVE_USER'
        if 'user' in message:
            user = message['user']
        return user

if __name__ == '__main__':
    config_manager = ConfigManager()
    conv_stage = ConversationsStage(config_manager)
    repl_stage = RepliesStage(config_manager)

    stage = Preprocess(config_manager)

    for channel, ts, conv in stage.main(repl_stage.main(conv_stage.main)):
        logger.info(f'Channel and ts: {channel}, {ts} returns conversation {conv}')