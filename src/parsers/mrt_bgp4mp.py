from src.models.route_update import PathAttributes, RouteUpdate, OriginType, Aggregator, ChangeType, AsPathType, AsPath, NLRI
from src.parsers.route_update import RouteUpdateParser
from collections import OrderedDict
from datetime import datetime
from mrtparse import Bgp4Mp

class MrtBgp4MpParser(RouteUpdateParser):
    def _parse_nlri(self, nlri: OrderedDict) -> NLRI:
        nlri = dict(nlri)
        
        return NLRI(
            prefix=nlri['prefix'],
            length=nlri['length'],
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

    def _parse_as_path(self, path_attributes: list[OrderedDict]) -> list[AsPath]:
        as_paths = self._get_path_attribute(
            path_attributes=path_attributes,
            type={2: 'AS_PATH'},
        )

        if as_paths is None:
            return None

        def _as_path_type(as_path: dict) -> AsPathType:
            match list(as_path['type'].values())[0]:
                case 'AS_SET':
                    return AsPathType.AS_SET
                case 'AS_SEQUENCE':
                    return AsPathType.AS_SEQUENCE
                case 'AS_CONFED_SET':
                    return AsPathType.AS_CONFED_SET
                case 'AS_CONFED_SEQUENCE':
                    return AsPathType.AS_CONFED_SEQUENCE

        return [
            AsPath(
                type=_as_path_type(dict(as_path)),
                value=[
                    int(value) 
                        for value in dict(as_path)['value']
                ],
            )
                for as_path in as_paths['value']
        ]

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

    def _parse_path_attributes(self, path_attributes: list[dict]) -> PathAttributes:
        return PathAttributes(
            origin=self._parse_origin(
                path_attributes=path_attributes,
            ),
            as_path=self._parse_as_path(
                path_attributes=path_attributes,
            ),
            next_hop=self._parse_next_hop(
                path_attributes=path_attributes,
            ),
            multi_exit_disc=self._parse_multi_exit_disc(
                path_attributes=path_attributes,
            ),
            atomic_aggregate=self._parse_atomic_aggregate(
                path_attributes=path_attributes,
            ),
            aggregator=self._parse_aggregator(
                path_attributes=path_attributes,
            ),
            community=self._parse_community(
                path_attributes=path_attributes,
            ),
            large_community=self._parse_large_community(
                path_attributes=path_attributes,
            ),
            extended_community=self._parse_extended_community(
                path_attributes=path_attributes,
            ),
        )

    def _parse_mp_reach_nlri(self, path_attributes: list[OrderedDict]) -> list[NLRI]:
        mp_reach_nlri = self._get_path_attribute(
            path_attributes=path_attributes,
            type={14: 'MP_REACH_NLRI'},
        )

        if mp_reach_nlri is None:
            return []
        
        mp_reach_nlri = dict(mp_reach_nlri['value'])

        return [
            self._parse_nlri(
                nlri=nlri,
            )
                for nlri in mp_reach_nlri['nlri']
        ]

    def _parse_mp_unreach_nlri(self, path_attributes: list[OrderedDict]) -> list[NLRI]:
        mp_unreach_nlri = self._get_path_attribute(
            path_attributes=path_attributes,
            type={15: 'MP_UNREACH_NLRI'},
        )

        if mp_unreach_nlri is None:
            return []
        
        mp_unreach_nlri = dict(mp_unreach_nlri['value'])

        return [
            self._parse_nlri(
                nlri=withdrawn_route,
            )
                for withdrawn_route in mp_unreach_nlri['withdrawn_routes']
        ]

    def parse(self, bgp4mp_message: Bgp4Mp) -> list[RouteUpdate]:
        route_updates: list[RouteUpdate] = []

        bgp4mp_message = dict(bgp4mp_message.data)
        nested_bgp4mp_message = dict(bgp4mp_message['bgp_message'])
        
        if nested_bgp4mp_message['type'].get(2) != 'UPDATE':
            return None
        
        generic_update = RouteUpdate(
            timestamp=datetime.fromtimestamp(
                timestamp=list(bgp4mp_message['timestamp'].keys())[0],
            ),
            peer_ip=bgp4mp_message['peer_ip'],
            local_ip=bgp4mp_message['local_ip'],
            peer_as=int(bgp4mp_message['peer_as']),
            local_as=int(bgp4mp_message['local_as']),
            path_attributes=self._parse_path_attributes(
                path_attributes=nested_bgp4mp_message.get('path_attributes', []),
            ),
        )

        # withdrawn routes
        for withdraw_route in nested_bgp4mp_message.get('withdrawn_routes', []) + self._parse_mp_unreach_nlri(
            path_attributes=nested_bgp4mp_message.get('path_attributes', []),
        ):
            route_updates.append(
                generic_update.model_copy(
                    update={
                        'change_type': ChangeType.WITHDRAW,
                        'nlri': self._parse_nlri(
                            nlri=withdraw_route,
                        ),
                    }
                )
            )

        # announce routes
        for announce_route in nested_bgp4mp_message.get('nlri', []) + self._parse_mp_reach_nlri(
            path_attributes=nested_bgp4mp_message.get('path_attributes', []),
        ):
            route_updates.append(
                generic_update.model_copy(
                    update={
                        'change_type': ChangeType.ANNOUNCE,
                        'nlri': self._parse_nlri(
                            nlri=announce_route,
                        ),
                    }
                )
            )

        self._send_messages(route_updates)
        return route_updates
