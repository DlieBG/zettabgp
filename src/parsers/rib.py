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
from src.parsers.route_update import RouteUpdateParser
from collections import OrderedDict
from datetime import datetime

class RibParser(RouteUpdateParser):
    '''
    This class is responsible for parsing RIB messages.

    Author:
        Benedikt Schwering <bes9584@thi.de>
        Sebastian Forstner <sef9869@thi.de>
    '''
    def _get_path_attribute(self, path_attributes: list[OrderedDict], type: dict) -> dict:
        for path_attribute in path_attributes:

            if path_attribute['type'] == type:
                return dict(path_attribute)

    def _parse_origin(self, path_attributes: list[OrderedDict]) -> OriginType:
        origin = self._get_path_attribute(
            path_attributes = path_attributes,
            type = {1: 'ORIGIN'},
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
    
    def _convert_to_ipv4(val: int) -> str:
        p1 = val >> 24
        p2 = (val - (p1 << 24)) >> 16
        p3 = (val - (p1 << 24) - (p2 << 16)) >> 8
        p4 = (val - (p1 << 24) - (p2 << 16) - (p3 << 8))

        ip = str(p1) + '.' + str(p2) + '.' + str(p3) + '.' + str(p4) 

        return ip
    
    def _parse_extended_community(self, path_attributes: list[OrderedDict]) -> list[str]:
        extended_community = self._get_path_attribute(
            path_attributes=path_attributes,
            type={16: 'EXTENDED COMMUNITIES'},
        )

        if extended_community is None:
            return None

        ext_communities: list[str] = []

        for ext in extended_community['value']:
            ext_type = format((ext >> 56), '#02x')
            ext_subtype = format(((ext >> 48)-((ext >> 56) << 8)), '#02x')
            ext_value = ext - ((ext >> 48) << 48)

            match ext_type:
                case '0x00' | '0x40' | '0x0' | '0x4':
                    # 2 octets used for global administration as AS number
                    # 4 octets used for local administration with unique value
                    ext_gl = ext_value >> 32
                    ext_loc = ext_value - (ext_gl << 32)
                    ext_str = str(ext_type) + ':' + str(ext_subtype) + ':' + str(ext_gl) + ':' + str(ext_loc)
                case '0x01' | '0x41':
                    # 4 octets used for global administration as IPv4 Address
                    # 2 octets used for local administration with unique value
                    ext_gl_num = ext_value >> 16
                    ext_loc = ext_value - (ext_gl_num << 16)
                    ext_gl_ip = self._convert_to_ipv4(
                        val=ext_gl_num,
                    )
                    ext_str = str(ext_type) + ':' + str(ext_subtype) + ':' + ext_gl_ip + ':' + str(ext_loc)
                case '0x02' | '0x42':
                    # 4 octets used for global administration as AS number
                    # 2 octets used for local administration with unique value
                    ext_gl = ext_value >> 16
                    ext_loc = ext_value - (ext_gl << 16)
                    ext_str = str(ext_type) + ':' + str(ext_subtype) + ':' + str(ext_gl) + ':' + str(ext_loc)
                case '0x03' | '0x43':
                    # Value separation not defined; last 6 octets can be used flexible
                    # Current representation as one number, because cant be separated without more knowledge
                    ext_str = str(ext_type) + ':' + str(ext_subtype) + ':' + str(ext_value) + ':'
                case _:
                    # Other types not represented in the most common cases
                    # Example: 0x80-0x8f and 0xc0-0xcf for experimental type
                    # Missing documentation for clear distinction
                    # Representation therefore like in previous case
                    ext_str = str(ext_type) + ':' + str(ext_subtype) + ':' + str(ext_value) + ':'

            ext_communities.append(ext_str)

        return ext_communities

    def _parse_path_attributes(self, rib_entrie: list[OrderedDict]) -> PathAttributes:
        return PathAttributes(
            origin = self._parse_origin(
                path_attributes = rib_entrie
            ),
            as_path=self._parse_as_path(
                path_attributes=rib_entrie,
            ),
            next_hop=self._parse_next_hop(
                path_attributes=rib_entrie,
            ),
            multi_exit_disc=self._parse_multi_exit_disc(
                path_attributes=rib_entrie,
            ),
            atomic_aggregate=self._parse_atomic_aggregate(
                path_attributes=rib_entrie,
            ),
            aggregator=self._parse_aggregator(
                path_attributes=rib_entrie,
            ),
            community=self._parse_community(
                path_attributes=rib_entrie,
            ),
            large_community=self._parse_large_community(
                path_attributes=rib_entrie,
            ),
            extended_community=self._parse_extended_community(
                path_attributes=rib_entrie,
            ),
        )

    def parse(self, statement: OrderedDict) -> list[RouteUpdate]:
        '''
        Parse a BGP4MP message.

        Author:
            Benedikt Schwering <bes9584@thi.de>
            Sebastian Forstner <sef9869@thi.de>

        Args:
            statement (OrderedDict): The RIB statement.

        Returns:
            list[RouteUpdate]: The parsed RouteUpdate objects.
        '''
        route_updates: list[RouteUpdate] = []

        if statement['subtype'].get(1) == 'PEER_INDEX_TABLE':
            return None
        
        rib_entries = statement['rib_entries']
        
        for entrie in rib_entries:
            generic_update = RouteUpdate(
                timestamp=datetime.fromtimestamp(
                    list((statement['timestamp'].keys()))[0]
                ),
                peer_ip='',
                local_ip=statement['prefix'],
                peer_as=0,
                local_as=0,
                path_attributes = self._parse_path_attributes(entrie['path_attributes']),
                change_type=ChangeType.ANNOUNCE,
                nlri=NLRI(
                    prefix=statement['prefix'],
                    length=statement['length'],
                ),
            )
            route_updates.append(generic_update) 

        self._send_messages(route_updates)
        return route_updates
