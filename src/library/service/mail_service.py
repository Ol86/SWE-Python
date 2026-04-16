"""Service for writing emails."""

from email.mime.text import MIMEText
from email.utils import make_msgid
from smtplib import SMTP, SMTPServerDisconnected
from socket import gaierror
from typing import Final
from uuid import uuid4

from loguru import logger

from library.config.mail import (
    mail_enabled,
    mail_host,
    mail_port,
    mail_timeout,
)
from library.service.member_dto import MemberDTO

__all__ = ["send_mail"]

MAIL_SERVER: Final = mail_host
MAIL_PORT: Final = mail_port
MAIL_SENDER: Final = "Python Server <python.server@acme.com>"
MAIL_RECEIVERS: Final = ["Buchhaltung <buchhaltung@acme.com>"]
MAIL_TIMEOUT: Final = mail_timeout


def send_mail(member_dto: MemberDTO) -> None:
    """Send an email with the member data.

    :param member_dto: The member data to send.
    """
    logger.debug("{}", member_dto)

    if not mail_enabled:
        logger.warning("Mail server is disabled. No mail will be sent.")
        return

    msg: Final = MIMEText(f"New Member: <b>{member_dto.last_name}</b>")
    msg["Subject"] = f"New Member: ID={member_dto.id}"
    msg["Message-ID"] = make_msgid(idstring=str(uuid4()))

    try:
        logger.debug("mailserver={}, port={}", MAIL_SERVER, MAIL_PORT)

        with SMTP(MAIL_SERVER, MAIL_PORT, timeout=MAIL_TIMEOUT) as smtp:
            smtp.sendmail(MAIL_SENDER, MAIL_RECEIVERS, msg.as_string())
            logger.info("msg={}", msg)
    except ConnectionRefusedError:
        logger.warning("Connection refused by mail server.")
    except SMTPServerDisconnected:
        logger.warning("Mail server disconnected.")
    except gaierror:
        logger.warning("socket.gaierror: Is server running in virtual network?")
