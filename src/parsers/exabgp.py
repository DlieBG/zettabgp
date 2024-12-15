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
from datetime import datetime
import json

class ExaBGPParser(RouteUpdateParser):
    '''
    This class is responsible for parsing ExaBGP messages.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    def _parse_origin(self, origin: str) -> OriginType:
        if origin is None:
            return None

        match origin:
            case 'igp':
                return OriginType.IGP
            case 'egp':
                return OriginType.EGP
            case 'incomplete':
                return OriginType.INCOMPLETE
    
    def _parse_as_path(self, as_path: list[int]) -> list[AsPath]:
        if as_path is None:
            return None

        # According to the ExaBGP documentation, the as-path attribute contains only as-sequences.
        # https://github.com/Exa-Networks/exabgp/wiki/Controlling-ExaBGP-:-API-for-received-messages#update-announcement-receive-routes
        return [
            AsPath(
                type=AsPathType.AS_SEQUENCE,
                value=as_path,
            )
        ]

    def _parse_aggregator(self, aggregator: str) -> Aggregator:
        if aggregator is None:
            return None

        return Aggregator(
            router_id=aggregator.split(':')[1],
            router_as=int(aggregator.split(':')[0]),
        )
    
    def _convert_to_ipv4(val: int) -> str:
        p1 = val >> 24
        p2 = (val - (p1 << 24)) >> 16
        p3 = (val - (p1 << 24) - (p2 << 16)) >> 8
        p4 = (val - (p1 << 24) - (p2 << 16) - (p3 << 8))

        ip = str(p1) + '.' + str(p2) + '.' + str(p3) + '.' + str(p4) 

        return ip
    
    def _parse_extended_community(self, extended_community: list[dict]) -> list[str]:
        if extended_community is None:
            return None
        
        ext_communities: list[str] = []

        for entry in extended_community:
            ext = entry['value']
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

    def _parse_path_attributes(self, exabgp_message: dict, next_hop: str = None) -> PathAttributes:
        attribute: dict = exabgp_message['neighbor']['message']['update'].get('attribute', {})

        return PathAttributes(
            # origin=self._parse_origin(
            #     origin=attribute.get('origin'),
            # ),
            as_path=self._parse_as_path(
                as_path=attribute.get('as-path'),
            ),
            # # According to the ExaBGP documentation, the next-hop attribute is only one ip address.
            # # https://github.com/Exa-Networks/exabgp/wiki/Controlling-ExaBGP-:-API-for-received-messages#update-announcement-receive-routes
            # next_hop=None if next_hop is None else [next_hop],
            # multi_exit_disc=attribute.get('med'),
            # local_pref=attribute.get('local-preference'),
            # atomic_aggregate=attribute.get('atomic-aggregate'),
            # aggregator=self._parse_aggregator(
            #     aggregator=attribute.get('aggregator'),
            # ),
            # community=attribute.get('community'),
            # large_community=attribute.get('large-community'),
            # extended_community=self._parse_extended_community(
            #     extended_community=attribute.get('extended-community'),
            # ),
            # orginator_id=attribute.get('originator-id'),
            # cluster_list=attribute.get('cluster-list'),
        )

    def parse(self, line: str) -> list[RouteUpdate]:
        '''
        Parse an ExaBGP message.

        Author:
            Benedikt Schwering <bes9584@thi.de>

        Args:
            line (str): The ExaBGP message.

        Returns:
            list[RouteUpdate]: The parsed RouteUpdate objects.
        '''
        route_updates: list[RouteUpdate] = []

        exabgp_message = json.loads(line)

        if exabgp_message['type'] != 'update':
            return None

        generic_update = RouteUpdate(
            timestamp=datetime.fromtimestamp(
                timestamp=exabgp_message['time'],
            ),
            peer_ip = exabgp_message['neighbor']['address']['peer'],
            local_ip = exabgp_message['neighbor']['address']['local'],
            peer_as = exabgp_message['neighbor']['asn']['peer'],
            local_as = exabgp_message['neighbor']['asn']['local'],
            path_attributes = self._parse_path_attributes(
                exabgp_message=exabgp_message,
            ),
        )

        # Iterate over the withdraw routes and create RouteUpdate objects
        for withdraw_routes in exabgp_message['neighbor']['message']['update'].get('withdraw', {}).values():
            for withdraw_route in withdraw_routes:
                route_updates.append(
                    generic_update.model_copy(
                        update={
                            'change_type': ChangeType.WITHDRAW,
                            'nlri': NLRI(
                                prefix=withdraw_route['nlri'].split('/')[0],
                                length=int(withdraw_route['nlri'].split('/')[1]),
                            ),
                        },
                    )
                )

        # Iterate over the announce routes and create RouteUpdate objects
        for announce_hops in exabgp_message['neighbor']['message']['update'].get('announce', {}).values():
            for announce_hop, announce_routes in announce_hops.items():
                for announce_route in announce_routes:
                    route_updates.append(
                        generic_update.model_copy(
                            update={
                                'path_attributes': self._parse_path_attributes(
                                    exabgp_message=exabgp_message,
                                    next_hop=announce_hop,
                                ),
                                'change_type': ChangeType.ANNOUNCE,
                                'nlri': NLRI(
                                    prefix=announce_route['nlri'].split('/')[0],
                                    length=int(announce_route['nlri'].split('/')[1]),
                                ),
                            },
                        )
                    )

        self._send_messages(route_updates)
        return route_updates
