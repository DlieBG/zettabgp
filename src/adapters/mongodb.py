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
from src.parsers.route_update import RouteUpdateParser
from src.models.route_update import RouteUpdate
from src.models.route_update import ChangeType
from pymongo import MongoClient
from typing import Optional
from bson import ObjectId
import os

class MongoDBAdapter:
    '''
    This class is responsible for receiving the parsed messages and forwarding them to both MongoDB databases.

    Author:
        Sebastian Forstner <sef9869@thi.de>
    '''
    def __init__(self, parser: RouteUpdateParser, no_mongodb_log: bool, no_mongodb_state: bool, no_mongodb_statistics: bool, clear_mongodb: bool):
        '''
        Initializes the MongoDBAdapter.

        Author:
            Sebastian Forstner <sef9869@thi.de>

        Args:
            parser (RouteUpdateParser): The parser to receive the parsed messages from.
            no_mongodb_log (bool): Whether to disable the log storage.
            no_mongodb_state (bool): Whether to disable the state storage.
            no_mongodb_statistics (bool): Whether to disable the statistics storage.
            clear_mongodb (bool): Whether to clear the MongoDB databases.
        '''
        try:
            # Connects to MongoDB-Container running with Docker
            database_client = MongoClient(
                host=os.getenv('MONGO_DB_HOST', 'localhost'),
                port=int(os.getenv('MONGO_DB_PORT', 27017)),
            )
        except:
            print('Could not connect to the database')

        log_flag = no_mongodb_log
        state_flag = no_mongodb_state
        statistics_flag = no_mongodb_statistics

        # Creates database and collection for log storage
        if not log_flag:
            log_db = database_client.message_log
            log_collection = log_db.storage
            if clear_mongodb:
                log_collection.delete_many({})
        
        # Creates database and collection for state storage
        if not state_flag:
            state_db = database_client.message_state
            state_collection = state_db.storage
            if clear_mongodb:
                state_collection.delete_many({})

        # Creates database and collection for statistics storage
        if not statistics_flag:
            statistics_db = database_client.message_statistics
            statistics_collection = statistics_db.storage
            if clear_mongodb:
                statistics_collection.delete_many({})

        @parser.on_update
        def on_update(message: RouteUpdate):

            # Saves optional, non-base-type attributes for later use; required to guarantee save use of mongodb
            if message.path_attributes.origin:
                origins = message.path_attributes.origin.value
            else:
                origins = None
            
            as_paths: Optional[list[int, list[int]]] = None
            if message.path_attributes.as_path:
                for as_pa in message.path_attributes.as_path:
                    if as_paths == None:
                        as_paths = [[as_pa.type.value, as_pa.value]]
                    else:
                        as_paths.append([as_pa.type.value, as_pa.value])
                 
            if message.path_attributes.aggregator:
                aggregator = {
                    'router_id' : message.path_attributes.aggregator.router_id,
                    'router_as' : message.path_attributes.aggregator.router_as,
                    }
            else:
                 aggregator = None

            extended_community: Optional[list[str]] = None
            if message.path_attributes.extended_community:
                for ext_com in message.path_attributes.extended_community:
                    if extended_community == None:
                        extended_community = [str(ext_com)]
                    else:
                        extended_community.append(str(ext_com)) 

            # Creates dict for message with _id and other unique attributes, that don't change
            new_message_id = {
                'timestamp' : message.timestamp,
                'peer_ip' : message.peer_ip,
                'local_ip' : message.local_ip,
                'peer_as' : message.peer_as,
                'local_as' : message.local_as,
                'change_type' : message.change_type.value,
                'nlri' : {
                    'prefix' : message.nlri.prefix,
                    'length' : message.nlri.length,
                },
                'path_attributes': {
                    'origin' : origins,
                    'as_path' : as_paths,
                    'next_hop' : message.path_attributes.next_hop,
                    'multi_exit_disc' : message.path_attributes.multi_exit_disc,
                    'local_pref' : message.path_attributes.local_pref,
                    'atomic_aggregate' : message.path_attributes.atomic_aggregate,
                    'aggregator' : aggregator,
                    'community' : message.path_attributes.community,
                    'large_community' : message.path_attributes.large_community,
                    'extended_community' : extended_community,
                    'orginator_id' : message.path_attributes.orginator_id,
                    'cluster_list' : message.path_attributes.cluster_list,
                },
                '_id' : ObjectId(),
            }

            # Creates dict used for collection updates, MUST NOT contain _id and should not contain other non changing attributes
            set_message = { 
                '$set': {
                    'timestamp' : message.timestamp,
                    'peer_ip' : message.peer_ip,
                    'peer_as' : message.peer_as,
                    'change_type' : message.change_type.value,
                    'path_attributes': {
                       'origin' : origins,
                        'as_path' : as_paths,
                        'next_hop' : message.path_attributes.next_hop,
                        'multi_exit_disc' : message.path_attributes.multi_exit_disc,
                        'local_pref' : message.path_attributes.local_pref,
                        'atomic_aggregate' : message.path_attributes.atomic_aggregate,
                        'aggregator' : aggregator,
                        'community' : message.path_attributes.community,
                        'large_community' : message.path_attributes.large_community,
                        'extended_community' : extended_community,
                        'orginator_id' : message.path_attributes.orginator_id,
                        'cluster_list' : message.path_attributes.cluster_list,
                    },
                }
            }

            # Route got withdrawn, db actions accordingly
            if message.change_type == ChangeType.WITHDRAW:
                if not log_flag:
                    log_announce = log_collection.insert_one(new_message_id)

                if not state_flag:
                    state_filter = {'nlri': {'prefix': new_message_id['nlri']['prefix'], 'length': new_message_id['nlri']['length']}}
                    state_announce = state_collection.delete_one(state_filter)

                if not statistics_flag:
                    statistics_filter = {'nlri': {'prefix': new_message_id['nlri']['prefix'], 'length': new_message_id['nlri']['length']}}
                    statistics_object = statistics_collection.find_one(statistics_filter)
                    if statistics_object:
                        new_values = {
                            '$set': {
                                'change_count' : statistics_object['change_count'] + 1,
                                'current_timestamp' : message.timestamp,
                                'last_timestamp' : statistics_object['current_timestamp'],
                            }
                        }
                    else:
                        new_values = {
                            '$set': {
                                'change_count' :1,
                                'current_timestamp' : message.timestamp,
                                'last_timestamp' : message.timestamp,
                                'nlri' : new_message_id['nlri'],
                                '_id' : ObjectId(),
                            }
                        }
                    statistics_announce = statistics_collection.update_one(statistics_filter, new_values, upsert=True)

            # Route got announced, db actions accordingly
            if message.change_type == ChangeType.ANNOUNCE:
                if not log_flag:
                    log_announce = log_collection.insert_one(new_message_id)

                if not state_flag:
                    state_filter = {'nlri': {'prefix': new_message_id['nlri']['prefix'], 'length': new_message_id['nlri']['length']}}
                    state_announce = state_collection.update_one(state_filter, set_message, upsert=True)
                
                if not statistics_flag:
                    statistics_filter = {'nlri': {'prefix': new_message_id['nlri']['prefix'], 'length': new_message_id['nlri']['length']}}
                    statistics_object = statistics_collection.find_one(statistics_filter)
                    if statistics_object:
                        new_values = {
                            '$set': {
                                'change_count' : (statistics_object['change_count'] + 1),
                                'current_timestamp' : message.timestamp,
                                'last_timestamp' : statistics_object['current_timestamp'],
                            }
                        }
                    else:
                        new_values = {
                            '$set': {
                                'change_count' :1,
                                'current_timestamp' : message.timestamp,
                                'last_timestamp' : message.timestamp,
                                'nlri' : new_message_id['nlri'],
                                '_id' : ObjectId(),
                            }
                        }  
                        statistics_announce = statistics_collection.update_one(statistics_filter, new_values, upsert=True)
