from src.models.update_message import BGPUpdateMessage, PathAttributes, OriginType, AsPathType, Aggregator, Network, AsPath
from src.parsers.update_message import BGPUpdateMessageParser
from datetime import datetime
from mrtparse import Bgp4Mp
from rich import print

class MrtBgp4MpParser(BGPUpdateMessageParser):
    def parse(self, bgp4mp_message: Bgp4Mp) -> BGPUpdateMessage:
        return BGPUpdateMessage()
