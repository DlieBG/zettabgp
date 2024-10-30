from src.models.route_update import RouteUpdate

class RouteUpdateParser:
    _on_update_functions = []

    def _send_messages(self, messages: list[RouteUpdate]):
        for message in messages:
            for fn in self._on_update_functions:
                fn(message)

    def on_update(self, fn):
        self._on_update_functions.append(fn)
