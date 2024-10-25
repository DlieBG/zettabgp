from src.models.update_message import BGPUpdateMessage

class BGPUpdateMessageParser:
    _on_update_functions = []

    def _send_message(self, message: BGPUpdateMessage):
        for fn in self._on_update_functions:
            fn(message)

    def on_update(self, fn):
        self._on_update_functions.append(fn)
