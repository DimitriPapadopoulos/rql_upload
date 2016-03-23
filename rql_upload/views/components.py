#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# CW import
from cubicweb.predicates import nonempty_rset, anonymous_user
from cubicweb.web import component

# RQL UPLOAD import
from utils import load_forms


###############################################################################
# CW upload box
###############################################################################

class CWUploadBox(component.CtxComponent):
    """ Class that generate a left box on the web browser to access all the
    decalred forms in the 'upload_structure_json' cubicweb instance parameter.

    It will appear on the left and contain the names if all forms defined in the
    json file.

    .. warning::

        It will NOT appear for anonymous users.
    """
    __regid__ = "ctx-upload-box"
    __select__ = (component.CtxComponent.__select__ & ~anonymous_user())
    title = _("Upload forms")
    context = "left"
    order = 0

    def render_body(self, w, **kwargs):
        """ Method that creates the upload navigation box (generates html code).

            This method displays error messages if the forms can't be extrated
            from the configuration file.
        """
        # Get the field form structure
        config = load_forms(self._cw.vreg.config)

        if config == -1:
            href = self._cw.build_url("view", vid="upload-view",
                                      title=self._cw._("Upload form"),
                                      form_name='ERROR: no json found')
            w(u'<div class="btn-toolbar">')
            w(u'<div class="btn-group-vertical btn-block">')
            w(u'<a class="btn btn-primary" href="{0}">'.format(href))
            w(u'{0}</a>'.format("ERROR: no json found."))
            w(u'</div></div>')

        elif config == -2:
            href = self._cw.build_url("view", vid="upload-view",
                                      title=self._cw._("Upload form"),
                                      form_name="ERROR: json file can't be read")
            w(u'<div class="btn-toolbar">')
            w(u'<div class="btn-group-vertical btn-block">')
            w(u'<a class="btn btn-primary" href="{0}">'.format(href))
            w(u"{0}</a>".format("ERROR: json file can't be read."))
            w(u'</div></div>')

        else:
            # Create a link to each form declared in the settings
            for form_name in config:
                href = self._cw.build_url("view", vid="upload-view",
                                          title=self._cw._("Upload form"),
                                          form_name=form_name)
                w(u'<div class="btn-toolbar">')
                w(u'<div class="btn-group-vertical btn-block">')
                w(u'<a class="btn btn-primary" href="{0}">'.format(href))
                w(u'{0}</a>'.format(form_name.title()))
                w(u'</div></div><br/>')
