#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


# System import
import os

# CW import
from cubicweb.server import hook
from cubicweb.server import hook
from cubicweb.predicates import is_instance


class UploadHook(hook.Hook):
    """ An upload entity is created/updated, store a fingerprint of binary data
    fields.
    """
    __regid__ = "rql_upload.upload"
    __select__ = hook.Hook.__select__ & is_instance("UploadFile", "UploadForm")
    events = ("before_add_entity", "before_update_entity")
    order = -1  # should be run before other hooks

    def __call__(self):
        """ If a 'data' field is uploaded, compute the associated fingerprint.
        """
        if "data" in self.entity.cw_edited:
            self.entity.set_format_and_encoding()
            data = self.entity.cw_edited["data"]
            if data is not None:
                data = self.entity.compute_sha1hex(data.getvalue())
            self.entity.cw_edited["data_sha1hex"] = data


class ServerStartupHook(hook.Hook):
    """ Deport files on file system rather than database indexation

    An 'UploadFile' entity data is deported on the server file system.
    To do so, we configure the 'UploadFile' 'data' attribute with the
    'BytesFileSystemStorage' storage.
    The repository location is defined at the instance creation
    'upload_directory' (instance parameter).
    If no instance parameter is set, the 'file' field won't be created.
    """
    __regid__ = "rql_upload.serverstartup"
    events = ("server_startup", "server_maintenance")

    def __call__(self):
        """ Configuring the 'BytesFileSystem' storage.
        """
        # In order sphinx to work properly: cw modify the path
        from cubicweb.server.sources import storages

        # Get the defined upload folder
        upload_dir = self.repo.vreg.config["upload_directory"]

        # Create the folder if necessary
        try:
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            # Configure the storage folder
            storage = storages.BytesFileSystemStorage(upload_dir)

            # Configure the storage file content
            storages.set_attribute_storage(self.repo, "UploadFile", "data",
                                           storage)
        except:
            pass
