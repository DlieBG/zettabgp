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
from src.models.route_update import PathAttributes, RouteUpdate, OriginType, Aggregator, ChangeType, AsPathType, AsPath, NLRI
from src.parsers.mrt_bgp4mp import MrtBgp4MpParser
from datetime import datetime
from mrtparse import Reader
import unittest, copy

class MrtBgp4MpParserTests(unittest.TestCase):
    '''
    Tests for the MRT BGP4MP parser.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    mrt_bgp4mp_parser = MrtBgp4MpParser()
    
    messages = [
        copy.copy(message)
            for message in Reader('tests/mrt/20241005_1800_1728151200_bgp_lw_ixp_decix_update')
    ]

    def test_announce_1(self):
        '''
        Test the parsing of a basic announce message.

        Author:
            Benedikt Schwering <bes9584@thi.de>
        '''
        self.assertEqual(
            first=self.mrt_bgp4mp_parser.parse(
                bgp4mp_message=self.messages[-1],
            ),
            second=[
                RouteUpdate(
                    timestamp=datetime.fromtimestamp(
                        timestamp=1728152101.0,
                    ),
                    peer_ip='80.81.193.157',
                    local_ip='80.81.192.183',
                    peer_as=6695,
                    local_as=39063,
                    path_attributes=PathAttributes(
                        origin=OriginType.IGP,
                        as_path=[
                            AsPath(
                                type=AsPathType.AS_SEQUENCE,
                                value=[
                                    6939,
                                    4826,
                                    60725,
                                    60725,
                                    60725,
                                    60725,
                                    60725,
                                    60725,
                                    12684,
                                    139898,
                                ],
                            ),
                        ],
                        next_hop=[
                            '80.81.192.172',
                        ],
                        multi_exit_disc=1392,
                        atomic_aggregate=True,
                        aggregator=Aggregator(
                            router_id='10.208.0.2',
                            router_as=64517,
                        ),
                        large_community=[
                            [6695, 1911, 90],
                            [6695, 1912, 0],
                            [6695, 1913, 276],
                            [6695, 1914, 150],
                        ],
                    ),
                    change_type=ChangeType.ANNOUNCE,
                    nlri=NLRI(
                        prefix='103.25.141.0',
                        length=24,
                    ),
                ),
            ],
        )
