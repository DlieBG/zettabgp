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
from typing import Optional

class ReverseParser(RouteUpdateParser):
    '''
    This class is responsible for parsing RIB messages.

    Author:
        Benedikt Schwering <bes9584@thi.de>
        Sebastian Forstner <sef9869@thi.de>
    '''
    def _parse_origin(self, orig_value: int) -> OriginType:
        if orig_value:
            match orig_value:
                case 1:
                    return OriginType.IGP
                case 2:
                    return OriginType.EGP
                case 3:
                    return OriginType.INCOMPLETE
                case _:
                    return None
        else:
            return None

    def _parse_as_path(self, as_paths: list[int, list[int]]) -> list[AsPath]:
        all_paths: Optional[list[AsPath]] = None
        if as_paths:
            for path in as_paths:
                path_type: AsPathType
                match path[0]:
                    case 1:
                        path_type = AsPathType.AS_SET
                    case 2:
                        path_type = AsPathType.AS_SEQUENCE
                    case 3:
                        path_type = AsPathType.AS_CONFED_SET
                    case 4:
                        path_type = AsPathType.AS_CONFED_SEQUENCE
                    case _:
                        return None
                new_path = AsPath(
                    type=path_type,
                    value=path[1]
                )
                if all_paths:
                    all_paths.append(new_path)
                else:
                    all_paths = [new_path]

        return all_paths

    def _parse_aggregator(self, aggregators: dict) -> Optional[Aggregator]:
        all_aggregators: Optional[Aggregator] = None
        if aggregators:
            # aggregators = dict(aggregators)
            new_aggregator = Aggregator(
                router_id=aggregators['router_id'],
                router_as=aggregators['router_as'],
            )

        return new_aggregator

    def _parse_extendet_community(self, ext_com: Optional[list[str]]) -> Optional[list[int]]:
        all_aggregators: Optional[list[int]] = None
        if ext_com:
            for com in ext_com:
                if all_aggregators:
                    all_aggregators.append(int(com))
                else:
                    all_aggregators = [int(com)]

        return all_aggregators

    def _parse_nlri(self, nlri: dict) -> NLRI:
        new_nlri = NLRI(
            prefix=nlri['prefix'],
            length=nlri['length'],
        )
        return new_nlri

    def _parse_change_type(self, ch_type: int) -> ChangeType:
        match ch_type:
            case 1:
                return ChangeType.ANNOUNCE
            case 2:
                return ChangeType.WITHDRAW
            case _:
                return None

    def parse(self, message_data: dict) -> list[RouteUpdate]:
        '''
        Parse a Database Log message.

        Author:
            Benedikt Schwering <bes9584@thi.de>
            Sebastian Forstner <sef9869@thi.de>

        Args:
            message_data (dict): The Database Log message.

        Returns:
            list[RouteUpdate]: The parsed RouteUpdate objects.
        '''
        route_updates: list[RouteUpdate] = []

        if message_data['path_attributes']['aggregator']:
            aggregators = self._parse_aggregator(dict(message_data['path_attributes']['aggregator']))
        else:
            aggregators = None
        new_path_attribute = PathAttributes(
            origin=self._parse_origin(message_data['path_attributes']['origin']),
            as_path=self._parse_as_path(message_data['path_attributes']['as_path']),
            next_hop=message_data['path_attributes']['next_hop'],
            multi_exit_disc=message_data['path_attributes']['multi_exit_disc'],
            local_pref=message_data['path_attributes']['local_pref'],
            atomic_aggregate=message_data['path_attributes']['atomic_aggregate'],
            aggregator=aggregators,
            community=message_data['path_attributes']['community'],
            large_community=message_data['path_attributes']['large_community'],
            extended_community=self._parse_extendet_community(message_data['path_attributes']['extended_community']),
            orginator_id=message_data['path_attributes']['orginator_id'],
            cluster_list=message_data['path_attributes']['cluster_list'],
        )
        new_route_update = RouteUpdate(
            timestamp=message_data['timestamp'],
            peer_ip=message_data['peer_ip'],
            local_ip=message_data['local_ip'],
            peer_as=message_data['peer_as'],
            local_as=message_data['local_as'],
            path_attributes=new_path_attribute,
            change_type=self._parse_change_type(message_data['change_type'][0]),
            nlri=self._parse_nlri(message_data['nlri']),
        )
        route_updates.append(new_route_update)

        self._send_messages(route_updates)
        return route_updates
