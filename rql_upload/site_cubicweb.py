#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


options = (
    (
        "upload_directory",
        {
            "type": "string",
            "default": "",
            "help": "base directory in which the files are uploaded.",
            "group": "rql_upload", "level": 0,
        }
    ),
    (
        "upload_structure_json",
        {
            "type": "string",
            "default": "",
            "help": "json file describing the different upload entities.",
            "group": "rql_upload", "level": 0,
        }
    ),
)
