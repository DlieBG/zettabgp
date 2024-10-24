from src.parsers.update_message import BGPUpdateMessageParser
from src.models.update_message import BGPUpdateMessage
from rich import print

class ExaBGPParser(BGPUpdateMessageParser):
    def parse(self, line: str):
        message = BGPUpdateMessage()

        print(message)
        self._send_message(message)
