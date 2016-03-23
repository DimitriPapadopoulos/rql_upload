#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import json
import os

# CW import
from cubicweb import ValidationError


def load_forms(cw_config):
    """ Function to load the forms structures from the file defined in the
    'upload_structure_json' cubicweb instance parameter.

    Parameters
    ----------
    cw_config: dict
        the cubicweb configuration built from the instance 'all-in-one.conf'
        file.

    Returns
    -------
    config: dict
        the forms descriptions defined in the 'upload_structure_json' setting
        file.
    -1
        if the file is not specified or found on the system.
    -2
        if the file cannot be decoded as json file.
    """
    config_file = cw_config["upload_structure_json"]
    if not os.path.isfile(config_file):
        # if file not found, return -1
        return -1
    try:
        with open(config_file) as open_json:
            config = json.load(open_json)

        return config
    except:
        # if file not readable as json, return -2
        return -2
