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
from fastapi import APIRouter
import pkg_resources

version_router = APIRouter()

@version_router.get('/')
def get_version() -> str:
    '''
    This function returns the version of the ZettaBGP package.

    Author:
        Benedikt Schwering <bes9584@thi.de>

    Returns:
        str: The version of the ZettaBGP package.
    '''
    return pkg_resources.get_distribution('zettabgp').version
