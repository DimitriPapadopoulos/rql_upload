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
import hashlib

# CW import
from cubicweb.entities import AnyEntity
from logilab.mtconverter import guess_mimetype_and_encoding


class EntityUploadFile(AnyEntity):
    """ Define the 'UploadFile' entity associated functions.
    """
    __regid__ = "UploadFile"

    def set_format_and_encoding(self):
        """ Try to set format and encoding according to known values (filename,
        file content, format, encoding).

        This method must be called in a before_[add|update]_entity hook else it
        won't have any effect.
        """
        return

    def compute_sha1hex(self, value=None):
        """ Compute a hash of the data.
        """
        if value is None and self.data is not None:
            value = self.data.getvalue()
        if value is not None:
            return unicode(hashlib.sha1(value).hexdigest())

    def dc_title(self):
        """ Method that defines the upload file entity title.
        """
        return self.data_name

    def icon_url(self):
        """ Method to get an icon for this entity.
        """
        return self._cw.data_url(os.path.join("icons", "upload.ico"))


class EntityUploadForm(AnyEntity):
    """ Define the 'UploadForm' entity associated functions.
    """
    __regid__ = "UploadForm"

    def set_format_and_encoding(self):
        """ Try to set format and encoding according to known values (filename,
        file content, format, encoding).

        This method must be called in a before_[add|update]_entity hook else it
        won't have any effect.
        """
        assert "data" in self.cw_edited, "missing mandatory attribute data"
        data_format, data_encoding = guess_mimetype_and_encoding(
                data=self.cw_edited.get("data"),
                # use get and not get_value since data has changed, we only want
                # to consider explicitly specified values, not old ones
                filename=self.cw_edited.get("data_name"),
                format=self.cw_edited.get("data_format"),  # encoding=encoding,
                fallbackencoding=self._cw.encoding)
        if data_format:
            self.cw_edited["data_format"] = unicode(data_format)
        if data_encoding:
            self.cw_edited["data_encoding"] = unicode(data_encoding)

    def compute_sha1hex(self, value=None):
        """ Compute a hash of the data.
        """
        if value is None and self.data is not None:
            value = self.data.getvalue()
        if value is not None:
            return unicode(hashlib.sha1(value).hexdigest())

    def dc_title(self):
        """ Method that defines the upload file entity title.
        """
        return self.data_name

    def icon_url(self):
        """ Method to get an icon for this entity.
        """
        return self._cw.data_url(os.path.join("icons", "upload.ico"))
