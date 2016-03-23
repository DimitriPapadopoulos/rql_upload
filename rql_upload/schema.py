##########################################################################
# NSAp - Copyright (C) CEA, 2013 - 2016
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# CubicWeb import
from yams.buildobjs import EntityType
from yams.buildobjs import String
from yams.buildobjs import Bytes
from yams.buildobjs import RichString
from yams.buildobjs import SubjectRelation
from cubicweb.schema import ERQLExpression
from cubicweb.schema import RQLUniqueConstraint


###############################################################################
# Modification of the schema
###############################################################################

UPLOAD_PERMISSIONS = {
    "read": (
        "managers",
        ERQLExpression("X uploaded_by U")),
    "add": ("managers", "users"),
    "update": ("managers", ),
    "delete": ("managers", ),
}


class UploadFile(EntityType):
    """ An entity used to upload file which may contain binary data.

    Attributes
    ----------
    title: String (optional)
        a short description of the file.
    data: Bytes (mandatory)
        contains the uploaded file.
    data_extension: String (mandatory)
        the uploaded file extension.
    data_name: String (mandatory)
        the uploaded file name.
    data_sha1hex: String (optional)
        SHA1 sum of the file.
    uploaded_by: SubjectRelation (mandatory)
        who has created the item.
    """
    # Set default permissions
    __permissions__ = UPLOAD_PERMISSIONS

    title = String(fulltextindexed=True, maxsize=256)
    data = Bytes(
        required=True, fulltextindexed=True,
        description=unicode("file to upload"))
    data_extension = String(
        required=True, maxsize=32,
        description=unicode("the upload file extension."))
    data_name = String(
        required=True, fulltextindexed=True,
        description=unicode("name of the file. Should be dynamically set at "
                            "upload time."))
    data_sha1hex = String(
        maxsize=40,
        description=unicode("SHA1 sum of the file. May be set at upload time."))
    description = RichString(fulltextindexed=True, internationalizable=True,
                             default_format="text/rest")

    # The link to the owner of the data
    uploaded_by = SubjectRelation(
        "CWUser", cardinality="1*", composite="subject")


class UploadForm(EntityType):
    """ A downloadable file.

    Attributes
    ----------
    title: String (optional)
        a short description of the file.
    data: Bytes (mandatory)
        contains the uploaded file.
    data_extension: String (mandatory)
        the uploaded file extension.
    data_name: String (mandatory)
        the uploaded file name.
    data_sha1hex: String (optional)
        SHA1 sum of the file.
    uploaded_by: SubjectRelation (mandatory)
        who has created the item.
    """
    # Set default permissions
    __permissions__ = UPLOAD_PERMISSIONS

    title = String(fulltextindexed=True, maxsize=256)
    data = Bytes(required=True, fulltextindexed=True,
                 description=unicode("file to upload"))
    data_format = String(
        required=True, maxsize=128,
        description=unicode("MIME type of the file. Should be dynamically set "
                            "at upload time."))
    data_encoding = String(
        maxsize=32,
        description=unicode("encoding of the file when it applies (e.g. text). "
                            "Should be dynamically set at upload time."))
    data_name = String(
        required=True, fulltextindexed=True,
        description=unicode("name of the file. Should be dynamically set at "
                            "upload time."))
    data_sha1hex = String(
        maxsize=40,
        description=unicode("SHA1 sum of the file. May be set at upload time."))
    description = RichString(fulltextindexed=True, internationalizable=True,
                             default_format="text/rest")

    # The link to the owner of the data
    uploaded_by = SubjectRelation(
        "CWUser", cardinality="1*", composite="subject")


class CWUpload(EntityType):
    """ An entity used to to store a form.

    Attributes
    ----------
    title: String (mandatory)
        the name of the upload (has to be unique in the data base).
    form_name: String (mandatory)
        the name of the form we upload.
    result_data: SubjectRelation (optional)
        the link(s) to the uploaded file.
    result_form: SubjectRelation (mandatory)
        the link to the form.
    uploaded_by: SubjectRelation (mandatory)
        who has created the item.
    """
    # Set default permissions
    __permissions__ = UPLOAD_PERMISSIONS

    # Entity parameters
    title = String(
        maxsize=256, required=True,
        constraints=[
            RQLUniqueConstraint(
                "X title N, S title N, X owned_by U, X is CWUpload",
                mainvars="X",
                msg=_("this name is already used"))
        ])
    form_name = String(maxsize=256, required=True)

    # The link to the uploaded data
    result_data = SubjectRelation(
        "UploadFile", cardinality="**", composite="subject")
    result_form = SubjectRelation(
        "UploadForm", cardinality="**", composite="subject")

    # The link to the owner of the data
    uploaded_by = SubjectRelation(
        "CWUser", cardinality="1*", composite="subject")
