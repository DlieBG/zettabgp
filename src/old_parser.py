from src.models.message import Message
import json

class BGPParser():
    '''This class is responsible for parsing the BGP messages and forwarding them to the appropriate adapter as parsed messages.'''
    _on_announce_functions = []
    _on_withdraw_functions = []

    def _send_message(self, fns, message: Message):
        '''This method sends a message to all registered functions.'''
        for fn in fns:
            fn(message)

    def parse(self, line: str):
        '''This method receives a line from ExaBGP, parses it to a Message object and hands it over to all registered on_message functions.'''
        message = json.loads(line)

        if message['type'] == 'update':
            message = Message.model_validate(
                obj=message['neighbor'],
            )

            if message.message.update:
                if message.message.update.announce:
                    self._send_message(
                        fns=self._on_announce_functions,
                        message=message,
                    )

                if message.message.update.withdraw:
                    self._send_message(
                        fns=self._on_withdraw_functions,
                        message=message,
                    )

    def on_announce(self, fn):
        '''This method registers a function to be called when a announce update message is parsed.'''
        self._on_announce_functions.append(fn)
    
    def on_withdraw(self, fn):
        '''This method registers a function to be called when a withdraw update message is parsed.'''
        self._on_withdraw_functions.append(fn)
