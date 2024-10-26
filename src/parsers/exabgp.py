from src.models.update_message import BGPUpdateMessage, PathAttributes, OriginType, AsPathType, Aggregator, Network, AsPath
from src.parsers.update_message import BGPUpdateMessageParser
from datetime import datetime
import itertools, json

class ExaBGPParser(BGPUpdateMessageParser):
    def _parse_origin(self, origin: str) -> OriginType:
        match origin:
            case 'igp':
                return OriginType.IGP
            case 'egp':
                return OriginType.EGP
            case 'incomplete':
                return OriginType.INCOMPLETE
    
    def _parse_as_path(self, as_path: list[int]) -> AsPath:
        if as_path is None:
            return None

        return AsPath(
            type=AsPathType.AS_SEQUENCE,
            value=as_path,
        )

    def _parse_next_hop(self, announce: dict) -> str:
        return list(
            itertools.chain.from_iterable([
                next_hops.keys() for next_hops in announce.values()
            ])
        )

    def _parse_aggregator(self, aggregator: str) -> Aggregator:
        if aggregator is None:
            return None

        return Aggregator(
            router_id=aggregator.split(':')[1],
            router_as=int(aggregator.split(':')[0]),
        )
    
    def _parse_extended_community(self, extended_community: list[dict]) -> list[int]:
        if extended_community is None:
            return None
        
        return [
            entry['value'] for entry in extended_community
        ]

    def parse(self, line: str) -> BGPUpdateMessage:
        exabgp_message = json.loads(line)
        update_message = BGPUpdateMessage(
            timestamp=datetime.fromtimestamp(
                timestamp=exabgp_message['time'],
            ),
        )

        if exabgp_message['type'] == 'update':
            update_message.peer_ip = exabgp_message['neighbor']['address']['peer']
            update_message.local_ip = exabgp_message['neighbor']['address']['local']
            update_message.peer_as = exabgp_message['neighbor']['asn']['peer']
            update_message.local_as = exabgp_message['neighbor']['asn']['local']

            # withdrawn routes
            if exabgp_message['neighbor']['message']['update'].get('withdraw'):
                for withdraw_routes in exabgp_message['neighbor']['message']['update']['withdraw'].values():
                    for withdraw_route in withdraw_routes:
                        update_message.withdrawn_routes.append(
                            Network(
                                prefix=withdraw_route['nlri'].split('/')[0],
                                mask=int(withdraw_route['nlri'].split('/')[1]),
                            )
                        )

            # path attributes
            if exabgp_message['neighbor']['message']['update'].get('announce'):
                announce = exabgp_message['neighbor']['message']['update']['announce']
                mp_reach_nlris: list[Network] = []

                for announce_hops in announce.values():
                    for announce_routes in announce_hops.values():
                        for announce_route in announce_routes:
                            mp_reach_nlris.append(
                                Network(
                                    prefix=announce_route['nlri'].split('/')[0],
                                    mask=int(announce_route['nlri'].split('/')[1]),
                                )
                            )

                if exabgp_message['neighbor']['message']['update'].get('attribute'):
                    attribute = exabgp_message['neighbor']['message']['update']['attribute']

                    update_message.path_attributes = PathAttributes(
                        origin=self._parse_origin(
                            origin=attribute['origin'],
                        ),
                        as_path=self._parse_as_path(
                            as_path=attribute.get('as-path'),
                        ),
                        next_hop=self._parse_next_hop(
                            announce=announce,
                        ),
                        multi_exit_disc=attribute.get('med', 0),
                        local_pref=attribute.get('local-preference', 100),
                        atomic_aggregate=attribute.get('atomic-aggregate', False),
                        aggregator=self._parse_aggregator(
                            aggregator=attribute.get('aggregator'),
                        ),
                        community=attribute.get('community'),
                        large_community=attribute.get('large-community'),
                        extended_community=self._parse_extended_community(
                            extended_community=attribute.get('extended-community'),
                        ),
                        orginator_id=attribute.get('originator-id'),
                        cluster_list=attribute.get('cluster-list'),
                        mp_reach_nlri=mp_reach_nlris,
                        mp_unreach_nlri=[],
                    )

            self._send_message(update_message)
            return update_message
