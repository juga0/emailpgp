# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:expandtab
# Copyright (C) 2018 juga <juga at riseup dot net> under MIT license

import logging
from emailpgp.mime.multipartpgp import MIMEMultipartPGP

logging.basicConfig()
logger = logging.getLogger('autocrypt')
logger.setLevel(logging.DEBUG)

MSG_MULTIPARTPGP = """Content-Type: multipart/encrypted; protocol="application/pgp-encrypted"; boundary="Y6fyGi9SoGeH8WwRaEdC6bbBcYOedDzrQ"
MIME-Version: 1.0

--Y6fyGi9SoGeH8WwRaEdC6bbBcYOedDzrQ
Content-Type: application/pgp-encrypted; Content-Description="PGP/MIME version identification"
MIME-Version: 1.0

Version: 1

--Y6fyGi9SoGeH8WwRaEdC6bbBcYOedDzrQ
Content-Type: application/octet-stream; name="encrypted.asc"; Content-Disposition="inline; filename="encrypted.asc""; Content-Description="OpenPGP encrypted message"
MIME-Version: 1.0

encryptedstr
--Y6fyGi9SoGeH8WwRaEdC6bbBcYOedDzrQ--
"""


def test_multipartpgp():
    encryptedstr = "encryptedstr"
    boundary = "Y6fyGi9SoGeH8WwRaEdC6bbBcYOedDzrQ"
    msg = MIMEMultipartPGP(encryptedstr, boundary=boundary)
    logger.debug(msg)
    # NOTE: because Content-Description and Content-Disposition
    # can change order, ignore it
    assert msg.as_string()[:9] == MSG_MULTIPARTPGP[:9]
    assert msg.as_string()[:11] == MSG_MULTIPARTPGP[:11]
