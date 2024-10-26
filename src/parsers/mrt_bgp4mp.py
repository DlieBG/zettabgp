from src.models.update_message import BGPUpdateMessage, PathAttributes, OriginType, AsPathType, Aggregator, Network, AsPath
from src.parsers.update_message import BGPUpdateMessageParser
from collections import OrderedDict
from datetime import datetime
from mrtparse import Bgp4Mp

class MrtBgp4MpParser(BGPUpdateMessageParser):
    def _parse_network(self, network: OrderedDict) -> Network:
        network = dict(network)
        
        return Network(
            prefix=network['prefix'],
            mask=network['length'],
        )
    
    def _get_path_attribute(self, path_attributes: OrderedDict, type: dict) -> dict:
        for path_attribute in path_attributes:
            path_attribute = dict(path_attribute)

            if path_attribute['type'] == type:
                return path_attribute
    
    def _parse_origin(self, path_attributes: list[OrderedDict]) -> OriginType:
        origin = self._get_path_attribute(
            path_attributes=path_attributes,
            type={1: 'ORIGIN'},
        )

        if origin is None:
            return None

        match list(origin['value'].values())[0]:
            case 'IGP':
                return OriginType.IGP
            case 'EGP':
                return OriginType.EGP
            case 'INCOMPLETE':
                return OriginType.INCOMPLETE

    def _parse_as_path(self, path_attributes: list[OrderedDict]) -> AsPath:
        as_path = self._get_path_attribute(
            path_attributes=path_attributes,
            type={2: 'AS_PATH'},
        )

        if as_path is None:
            return None

        as_path = dict(as_path['value'][0])

        def _type() -> AsPathType:
            match list(as_path['type'].values())[0]:
                case 'AS_SET':
                    return AsPathType.AS_SET
                case 'AS_SEQUENCE':
                    return AsPathType.AS_SEQUENCE
                case 'AS_CONFED_SET':
                    return AsPathType.AS_CONFED_SET
                case 'AS_CONFED_SEQUENCE':
                    return AsPathType.AS_CONFED_SEQUENCE

        return AsPath(
            type=_type(),
            value=[
                int(value) 
                    for value in as_path['value']
            ],
        )

    def _parse_next_hop(self, path_attributes: list[OrderedDict]) -> list[str]:
        next_hop = self._get_path_attribute(
            path_attributes=path_attributes,
            type={3: 'NEXT_HOP'},
        )
        mp_reach_nlri = self._get_path_attribute(
            path_attributes=path_attributes,
            type={14: 'MP_REACH_NLRI'},
        )

        if next_hop:
            return [next_hop['value']]

        if mp_reach_nlri:
            mp_reach_nlri = dict(mp_reach_nlri['value'])

            return mp_reach_nlri['next_hop']
            
        return None
    
    def _parse_multi_exit_disc(self, path_attributes: list[OrderedDict]) -> int:
        multi_exit_disc = self._get_path_attribute(
            path_attributes=path_attributes,
            type={4: 'MULTI_EXIT_DISC'},
        )

        if multi_exit_disc is None:
            return 0

        return multi_exit_disc['value']

    def _parse_atomic_aggregate(self, path_attributes: list[OrderedDict]) -> int:
        atomic_aggregate = self._get_path_attribute(
            path_attributes=path_attributes,
            type={6: 'ATOMIC_AGGREGATE'},
        )

        if atomic_aggregate is None:
            return False

        return atomic_aggregate['value'] == ''

    def _parse_aggregator(self, path_attributes: list[OrderedDict]) -> Aggregator:
        aggregator = self._get_path_attribute(
            path_attributes=path_attributes,
            type={7: 'AGGREGATOR'},
        )

        if aggregator is None:
            return None

        aggregator = dict(aggregator['value'])

        return Aggregator(
            router_id=aggregator['id'],
            router_as=int(aggregator['as']),
        )
    
    def _parse_community(self, path_attributes: list[OrderedDict]) -> list[list[int]]:
        community = self._get_path_attribute(
            path_attributes=path_attributes,
            type={8: 'COMMUNITY'},
        )

        if community is None:
            return None

        return [
            [
                int(v)
                    for v in c.split(':')
            ]
                for c in community['value']
        ]

    def _parse_large_community(self, path_attributes: list[OrderedDict]) -> list[list[int]]:
        large_community = self._get_path_attribute(
            path_attributes=path_attributes,
            type={32: 'LARGE_COMMUNITY'},
        )

        if large_community is None:
            return None

        return [
            [
                int(v)
                    for v in c.split(':')
            ]
                for c in large_community['value']
        ]

    def _parse_extended_community(self, path_attributes: list[OrderedDict]) -> list[int]:
        extended_community = self._get_path_attribute(
            path_attributes=path_attributes,
            type={16: 'EXTENDED COMMUNITIES'},
        )

        if extended_community is None:
            return None

        return extended_community['value']

    def _parse_mp_reach_nlri(self, nested_bgp4mp_message: dict) -> list[Network]:
        if len(nested_bgp4mp_message['nlri']) > 0:
            return [
                self._parse_network(
                    network=nlri,
                )
                    for nlri in nested_bgp4mp_message['nlri']
            ]

        mp_reach_nlri = self._get_path_attribute(
            path_attributes=nested_bgp4mp_message['path_attributes'],
            type={14: 'MP_REACH_NLRI'},
        )

        if mp_reach_nlri:
            mp_reach_nlri = dict(mp_reach_nlri['value'])

            return [
                self._parse_network(
                    network=nlri,
                )
                    for nlri in mp_reach_nlri['nlri']
            ]

        return []

    def _parse_mp_unreach_nlri(self, path_attributes: list[OrderedDict]) -> list[Network]:
        mp_unreach_nlri = self._get_path_attribute(
            path_attributes=path_attributes,
            type={15: 'MP_UNREACH_NLRI'},
        )

        if mp_unreach_nlri is None:
            return []
        
        mp_unreach_nlri = dict(mp_unreach_nlri['value'])

        return [
            self._parse_network(
                network=withdrawn_route,
            )
                for withdrawn_route in mp_unreach_nlri['withdrawn_routes']
        ]

    def parse(self, bgp4mp_message: Bgp4Mp) -> BGPUpdateMessage:
        bgp4mp_message = dict(bgp4mp_message.data)
        update_message = BGPUpdateMessage(
            timestamp=datetime.fromtimestamp(
                timestamp=list(bgp4mp_message['timestamp'].keys())[0],
            ),
            peer_ip=bgp4mp_message['peer_ip'],
            local_ip=bgp4mp_message['local_ip'],
            peer_as=int(bgp4mp_message['peer_as']),
            local_as=int(bgp4mp_message['local_as']),
        )

        nested_bgp4mp_message = dict(bgp4mp_message['bgp_message'])

        if nested_bgp4mp_message['type'].get(2) == 'UPDATE':
            # withdrawn routes
            update_message.withdrawn_routes = [
                self._parse_network(
                    network=withdrawn_route,
                )
                    for withdrawn_route in nested_bgp4mp_message['withdrawn_routes']
            ]

            # path attributes
            if len(nested_bgp4mp_message['path_attributes']) > 0:
                update_message.path_attributes = PathAttributes(
                    origin=self._parse_origin(
                        path_attributes=nested_bgp4mp_message['path_attributes'],
                    ),
                    as_path=self._parse_as_path(
                        path_attributes=nested_bgp4mp_message['path_attributes'],
                    ),
                    next_hop=self._parse_next_hop(
                        path_attributes=nested_bgp4mp_message['path_attributes'],
                    ),
                    multi_exit_disc=self._parse_multi_exit_disc(
                        path_attributes=nested_bgp4mp_message['path_attributes'],
                    ),
                    atomic_aggregate=self._parse_atomic_aggregate(
                        path_attributes=nested_bgp4mp_message['path_attributes'],
                    ),
                    aggregator=self._parse_aggregator(
                        path_attributes=nested_bgp4mp_message['path_attributes'],
                    ),
                    community=self._parse_community(
                        path_attributes=nested_bgp4mp_message['path_attributes'],
                    ),
                    large_community=self._parse_large_community(
                        path_attributes=nested_bgp4mp_message['path_attributes'],
                    ),
                    extended_community=self._parse_extended_community(
                        path_attributes=nested_bgp4mp_message['path_attributes'],
                    ),
                    mp_reach_nlri=self._parse_mp_reach_nlri(
                        nested_bgp4mp_message=nested_bgp4mp_message,
                    ),
                    mp_unreach_nlri=self._parse_mp_unreach_nlri(
                        path_attributes=nested_bgp4mp_message['path_attributes'],
                    ),
                )

        self._send_message(update_message)
        return update_message
