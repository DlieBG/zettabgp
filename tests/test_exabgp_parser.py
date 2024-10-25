from src.models.update_message import BGPUpdateMessage, PathAttributes, OriginType, AsPathType, Aggregator, Network, AsPath
from src.parsers.exabgp import ExaBGPParser
from datetime import datetime
import unittest

class ExaBGPParserTests(unittest.TestCase):
    exabgp_parser = ExaBGPParser()

    def test_announce_basic_1(self):
        self.assertEqual(
            first=self.exabgp_parser.parse(
                line='{ "exabgp": "4.0.1", "time": 1729362675.303443, "host" : "node103", "pid" : 41610, "ppid" : 41609, "counter": 18, "type": "update", "neighbor": { "address": { "local": "172.17.179.103", "peer": "172.17.179.104" }, "asn": { "local": 1, "peer": 1 } , "direction": "receive", "message": { "update": { "attribute": { "origin": "igp", "local-preference": 100 }, "announce": { "ipv4 unicast": { "172.17.179.104": [ { "nlri": "1.1.0.0/24" } ] } } } } } }',
            ),
            second=BGPUpdateMessage(
                timestamp=datetime.fromtimestamp(1729362675.303443),
                peer_ip='172.17.179.104',
                local_ip='172.17.179.103',
                peer_as=1,
                local_as=1,
                withdrawn_routes=[],
                path_attributes=[
                    PathAttributes(
                        origin=OriginType.IGP,
                        next_hop=[
                            '172.17.179.104',
                        ],
                        local_pref=100,
                        mp_reach_nlri=[
                            Network(
                                prefix='1.1.0.0',
                                mask=24,
                            ),
                        ],
                    ),
                ],
            ),
        )

    def test_announce_basic_2(self):
        self.assertEqual(
            first=self.exabgp_parser.parse(
                line='{ "exabgp": "4.0.1", "time": 1729362676.3019273, "host" : "node103", "pid" : 41610, "ppid" : 41609, "counter": 19, "type": "update", "neighbor": { "address": { "local": "172.17.179.103", "peer": "172.17.179.104" }, "asn": { "local": 1, "peer": 1 } , "direction": "receive", "message": { "update": { "attribute": { "origin": "igp", "local-preference": 100 }, "announce": { "ipv4 unicast": { "172.17.179.104": [ { "nlri": "1.1.0.0/25" } ] } } } } } }',
            ),
            second=BGPUpdateMessage(
                timestamp=datetime.fromtimestamp(1729362676.3019273),
                peer_ip='172.17.179.104',
                local_ip='172.17.179.103',
                peer_as=1,
                local_as=1,
                withdrawn_routes=[],
                path_attributes=[
                    PathAttributes(
                        origin=OriginType.IGP,
                        next_hop=[
                            '172.17.179.104',
                        ],
                        local_pref=100,
                        mp_reach_nlri=[
                            Network(
                                prefix='1.1.0.0',
                                mask=25,
                            ),
                        ],
                    ),
                ],
            ),
        )

    def test_announce_large_community(self):
        self.assertEqual(
            first=self.exabgp_parser.parse(
                line='{ "exabgp": "4.0.1", "time": 1729363609.4892604, "host" : "node103", "pid" : 41733, "ppid" : 41732, "counter": 34, "type": "update", "neighbor": { "address": { "local": "172.17.179.103", "peer": "172.17.179.104" }, "asn": { "local": 1, "peer": 1 } , "direction": "receive", "message": { "update": { "attribute": { "origin": "igp", "as-path": [ 12779, 12654 ], "confederation-path": [], "med": 1110, "local-preference": 100, "aggregator": "64521:10.6.39.0", "community": [ [ 12779, 10401 ], [ 12779, 65000 ] ], "large-community": [ [ 6695, 1911 , 172 ], [ 6695, 1912 , 0 ], [ 6695, 1913 , 276 ], [ 6695, 1914 , 150 ] ] }, "announce": { "ipv6 unicast": { "2001:7f8::31eb:0:1": [ { "nlri": "2001:7fb:fe15::/48" } ] } } } } } }',
            ),
            second=BGPUpdateMessage(
                timestamp=datetime.fromtimestamp(1729363609.4892604),
                peer_ip='172.17.179.104',
                local_ip='172.17.179.103',
                peer_as=1,
                local_as=1,
                withdrawn_routes=[],
                path_attributes=[
                    PathAttributes(
                        origin=OriginType.IGP,
                        as_path=AsPath(
                            type=AsPathType.AS_SEQUENCE,
                            value=[
                                12779,
                                12654,
                            ],
                        ),
                        next_hop=[
                            '2001:7f8::31eb:0:1',
                        ],
                        multi_exit_disc=1110,
                        local_pref=100,
                        aggregator=Aggregator(
                            router_id='10.6.39.0',
                            router_as=64521,
                        ),
                        community=[
                            [
                                12779,
                                10401,
                            ],
                            [
                                12779,
                                65000,
                            ],
                        ],
                        large_community=[
                            [
                                6695,
                                1911,
                                172,
                            ],
                            [
                                6695,
                                1912,
                                0,
                            ],
                            [
                                6695,
                                1913,
                                276,
                            ],
                            [
                                6695,
                                1914,
                                150,
                            ],
                        ],
                        mp_reach_nlri=[
                            Network(
                                prefix='2001:7fb:fe15::',
                                mask=48,
                            ),
                        ],
                    ),
                ],
            ),
        )
    
    def test_withdraw_basic(self):
        self.assertEqual(
            first=self.exabgp_parser.parse(
                line='{ "exabgp": "4.0.1", "time": 1729362677.302448, "host" : "node103", "pid" : 41610, "ppid" : 41609, "counter": 20, "type": "update", "neighbor": { "address": { "local": "172.17.179.103", "peer": "172.17.179.104" }, "asn": { "local": 1, "peer": 1 } , "direction": "receive", "message": { "update": { "withdraw": { "ipv4 unicast": [ { "nlri": "1.1.0.0/24" } ] } } } } }',
            ),
            second=BGPUpdateMessage(
                timestamp=datetime.fromtimestamp(1729362677.302448),
                peer_ip='172.17.179.104',
                local_ip='172.17.179.103',
                peer_as=1,
                local_as=1,
                withdrawn_routes=[
                    Network(
                        prefix='1.1.0.0',
                        mask=24,
                    ),
                ],
                path_attributes=[],
            ),
        )
