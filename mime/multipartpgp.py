# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab
# Copyright (C) 2017 juga <juga at riseup dot net> under MIT license
# Base on python email.mime classes:
# https://github.com/python/cpython/blob/6f0eb93183519024cb360162bdd81b9faec97ba6/Lib/email/mime/multipart.py
# https://github.com/python/cpython/blob/6f0eb93183519024cb360162bdd81b9faec97ba6/Lib/email/mime/application.py

"""Extend Python email classes for MIME multipart/pgp-encrypted
type messages.
"""

__all__ = ['MIMEMultipartPGP', 'MIMEApplicationPGPPayload',
           'MIMEApplicationPGPDescription']

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email import encoders
from email import policy


class MIMEMultipartPGP(MIMEMultipart):
    """Base class for MIME multipart/encrypted type messages."""

    def __init__(self, _data=None, _subtype='encrypted', boundary=None,
                 *, policy=policy.default, **_params):
        """Creates a multipart/encrypted type message.

        By default, creates a multipart/encrypted message, with proper
        Content-Type and MIME-Version headers.

        _subtype is the subtype of the multipart content type, defaulting to
        `encrypted'.

        boundary is the multipart boundary string.  By default it is
        calculated as needed.

        _data is a string containing the raw payload data (encrypted).

        Additional parameters for the Content-Type header are taken from the
        keyword arguments (or passed into the _params argument).

        It will create the Email structure:
        └┬╴multipart/encrypted
         ├─╴application/pgp-encrypted
         └─╴application/octet-stream inline [encrypted.asc]
         """
        _params['protocol'] = "application/pgp-encrypted"
        description = MIMEApplicationPGPDescription()
        payload = MIMEApplicationPGPPayload(_data)
        _subparts = [description, payload]
        MIMEMultipart.__init__(self, _subtype, boundary, _subparts,
                               policy=policy, **_params)


class MIMEApplicationPGPPayload(MIMEApplication):
    """Class for generating application/octet-stream MIME documents."""

    def __init__(self, _data,
                 _subtype='octet-stream; name="encrypted.asc"',
                 _encoder=encoders.encode_noop, *, policy=None, **_params):
        """Create an application/octet-stream type MIME document.

        _data is a string containing the raw application data.

        _subtype is the MIME content type subtype, defaulting to
        'octet-stream; name="encrypted.asc"'.

        _encoder is a function which will perform the actual encoding for
        transport of the application data, defaulting to noop encoding.

        Any additional keyword arguments are passed to the base class
        constructor, which turns them into parameters on the Content-Type
        header.
        """
        _params["Content-Description"] = "OpenPGP encrypted message"
        _params["Content-Disposition"] = 'inline; filename="encrypted.asc"'
        MIMEApplication.__init__(self, _data, _subtype, _encoder,
                                 policy=policy, **_params)


class MIMEApplicationPGPDescription(MIMEApplication):
    """Class for generating application/pgp-encrypted MIME documents."""

    def __init__(self, _data="Version: 1\n", _subtype='pgp-encrypted',
                 _encoder=encoders.encode_noop, *, policy=None, **_params):
        """Create an application/pgp-encrypted type MIME document.

        _data is a string containing by default Version: 1\n.

        _subtype is the MIME content type subtype, defaulting to
        'pgp/encrypted'.

        _encoder is a function which will perform the actual encoding for
        transport of the application data, defaulting to noop encoding.

        Any additional keyword arguments are passed to the base class
        constructor, which turns them into parameters on the Content-Type
        header.
        """
        _params["Content-Description"] = "PGP/MIME version identification"
        MIMEApplication.__init__(self, _data, _subtype, _encoder,
                                 policy=policy, **_params)
