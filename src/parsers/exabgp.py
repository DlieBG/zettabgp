from src.models.route_update import PathAttributes, RouteUpdate, OriginType, Aggregator, ChangeType, AsPathType, AsPath, NLRI
from src.parsers.route_update import RouteUpdateParser
from datetime import datetime
import json

class ExaBGPParser(RouteUpdateParser):
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
    
    def _parse_extended_community(self, extended_community: list[dict]) -> list[int]:
        if extended_community is None:
            return None
        
        return [
            entry['value'] for entry in extended_community
        ]

    def _parse_path_attributes(self, exabgp_message: dict, next_hop: str = None) -> PathAttributes:
        attribute: dict = exabgp_message['neighbor']['message']['update'].get('attribute', {})

        return PathAttributes(
            origin=self._parse_origin(
                origin=attribute.get('origin'),
            ),
            as_path=self._parse_as_path(
                as_path=attribute.get('as-path'),
            ),
            next_hop=None if next_hop is None else [next_hop],
            multi_exit_disc=attribute.get('med'),
            local_pref=attribute.get('local-preference'),
            atomic_aggregate=attribute.get('atomic-aggregate'),
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
        )

    def parse(self, line: str) -> list[RouteUpdate]:
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

        # withdrawn routes
        for withdraw_routes in exabgp_message['neighbor']['message']['update'].get('withdraw', {}).values():
            for withdraw_route in withdraw_routes:
                withdraw_message = generic_update

                withdraw_message.change_type = ChangeType.WITHDRAW
                withdraw_message.nlri = NLRI(
                        prefix=withdraw_route['nlri'].split('/')[0],
                        length=int(withdraw_route['nlri'].split('/')[1]),
                )

                route_updates.append(withdraw_message)

        # announce routes
        for announce_hops in exabgp_message['neighbor']['message']['update'].get('announce', {}).values():
            for announce_hop, announce_routes in announce_hops.items():
                for announce_route in announce_routes:
                    announce_message = generic_update

                    announce_message.path_attributes = self._parse_path_attributes(
                        exabgp_message=exabgp_message,
                        next_hop=announce_hop,
                    )
                    announce_message.change_type = ChangeType.ANNOUNCE
                    announce_message.nlri = NLRI(
                        prefix=announce_route['nlri'].split('/')[0],
                        length=int(announce_route['nlri'].split('/')[1]),
                    )

                    route_updates.append(announce_message)

        self._send_messages(route_updates)
        return route_updates
