# -*- coding: utf-8 -*-
'''
ZettaBGP - Advanced Anomaly Detection in Internet Routing
Copyright (c) 2024 Benedikt Schwering and Sebastian Forstner

This work is licensed under the terms of the MIT license.
For a copy, see LICENSE in the project root.

Author:
    Benedikt Schwering <bes9584@thi.de>
    Sebastian Forstner <sef9869@thi.de>
'''
from src.models.route_update import RouteUpdate

class RouteUpdateParser:
    '''
    This class defines a common interface for all route update parsers.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    _on_update_functions = []

    def _send_messages(self, messages: list[RouteUpdate]):
        for message in messages:
            for fn in self._on_update_functions:
                fn(message)

    def on_update(self, fn):
        '''
        Register a function that should be called when a new route update is parsed.

        Author:
            Benedikt Schwering <bes9584@thi.de>

        Args:
            fn: The function that should be called when a new route update is parsed.
        '''
        self._on_update_functions.append(fn)
