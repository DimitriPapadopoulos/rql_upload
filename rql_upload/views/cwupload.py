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
import re

# CW import
from cgi import parse_qs
from logilab.mtconverter import xml_escape
from logilab.common.decorators import monkeypatch
from cubicweb import Binary
from cubicweb.view import View
from cubicweb.web import Redirect
from cubicweb.web import formfields
from cubicweb.web import formwidgets
from cubicweb.web import RequestError
from cubicweb.web.views.forms import FieldsForm
from cubicweb.web.views.formrenderers import FormRenderer

# RQL UPLOAD import
from utils import load_forms


###############################################################################
# CWSearch Widgets
###############################################################################

class CWUploadForm(FieldsForm):
    """ Allowed fields

    Basic fields
    ------------

    .. autoclass:: cubicweb.web.formfields.StringField()
    .. autoclass:: cubicweb.web.formfields.PasswordField()
    .. autoclass:: cubicweb.web.formfields.IntField()
    .. autoclass:: cubicweb.web.formfields.BigIntField()
    .. autoclass:: cubicweb.web.formfields.FloatField()
    .. autoclass:: cubicweb.web.formfields.BooleanField()
    .. autoclass:: cubicweb.web.formfields.DateField()
    .. autoclass:: cubicweb.web.formfields.DateTimeField()
    .. autoclass:: cubicweb.web.formfields.TimeField()
    .. autoclass:: cubicweb.web.formfields.TimeIntervalField()

    Compound fields
    ---------------

    .. autoclass:: cubicweb.web.formfields.RichTextField()
    .. autoclass:: cubicweb.web.formfields.FileField()
    .. autoclass:: cubicweb.web.formfields.CompoundField()
    """
    __regid__ = "upload-form"

    form_buttons = [formwidgets.SubmitButton(cwaction="apply")]
    upload_title = formfields.StringField(
        name="upload_title", label="Title", required=True, value="<unique>")


@monkeypatch(FormRenderer)
def render_content(self, w, form, values):
    """ Overwrite the original loading message.
    """
    if self.display_progress_div:
        w(u'<div id="progress" class="alert alert-warning">')
        w(u'<img width="50" src="{0}"/>'.format(
              self._cw.build_url('data/images/uploading.gif')))
        w(u'<b>Work in progress, please wait ...</b>')
        w(u'</div>')

    self.render_fields(w, form, values)
    self.render_buttons(w, form)


class CWUploadView(View):
    """ Custom widget to edit the form from the configuration file.
    """
    __regid__ = "upload-view"

    bool_map = {
        "True": True,
        "False": False
    }

    def call(self, **kwargs):
        """ Create the 'form' fields.
        """
        # Get some parameters
        path = self._cw.relative_path()
        if "?" in path:
            path, param = path.split("?", 1)
            kwargs.update(parse_qs(param))
        form_name = kwargs["form_name"][0]

        # Get the form fields
        config = load_forms(self._cw.vreg.config)

        # Create a structure to store values that must be checked before the 
        # insertion in the data base
        check_struct = {}

        # Create the form       
        form = self._cw.vreg["forms"].select(
            "upload-form", self._cw, action="", form_name=form_name)
        for field in config[form_name]:
            field_type = field.pop("type")
            if field_type == "BooleanField" and "value" in field:
                field["value"] = self.bool_map[field["value"]]
            if "required" in field:
                field["required"] = self.bool_map[field["required"]]
            if "check_value" in field:
                check_struct[field["name"]] = field.pop("check_value")
            form.append_field(formfields.__dict__[field_type](**field))

        # Form processings
        try:
            posted = form.process_posted()

            # Get the form parameters
            inline_params = {}
            deported_params = {}
            for field_name, field_value in posted.iteritems():                  

                # Filter fields stored in the db or deported on the filesystem
                if isinstance(field_value, Binary):
                    # Check if the field value is valid
                    if field_name in check_struct:
                        file_name = self._cw.form[field_name][0]
                        if re.match(check_struct[field_name],
                                    file_name) is None:
                            raise RequestError(
                                "Find wrong file name '{0}' while searching "
                                "for pattern '{1}'".format(
                                    file_name, check_struct[field_name]))

                    # Add fs item
                    deported_params[field_name] = field_value
                else:
                    # Check if the field value is valid
                    if field_name in check_struct:
                        if re.match(check_struct[field_name],
                                    str(field_value)) is None:
                            raise RequestError()

                    # Add db item
                    inline_params[field_name] = field_value

            # Save the inline parameters in a File entity
            form_eid = self._cw.create_entity(
                "File", data=Binary(json.dumps(inline_params)),
                data_format=u"text/json", data_name=u"form.json").eid

            # Save deported parameters in UploadFile entities
            upload_file_eids = []
            for field_name, field_value in deported_params.iteritems():
                file_name = self._cw.form[field_name][0]
                basename, extension = os.path.splitext(file_name)
                upload_file_eids.append(self._cw.create_entity(
                    "UploadFile", data=field_value, title=unicode(basename),
                    data_extension=unicode(extension[1:]),
                    data_name=unicode(file_name)).eid)

            # Create the CWUpload entity
            upload_eid = self._cw.create_entity(
                "CWUpload", title=unicode(inline_params["upload_title"]),
                form_name=unicode(form_name), result_form=form_eid,
                result_data=upload_file_eids).eid
            
            # Redirection to the created CWUpload entity
            raise Redirect(self._cw.build_url(eid=upload_eid))
        except RequestError as error:
            self.w(u"<p>{0}</p>".format(error))

        # Form rendering
        self.w(u'<h3 class="panel-title">Upload ("{0}" form)</h3>'.format(
            form_name))
        form.render(w=self.w, formvalues=self._cw.form)

