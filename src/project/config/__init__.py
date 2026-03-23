"""
This module provides configuration settings for the server and TLS.
It imports the necessary configuration values from the respective modules and makes them available for use in the application.
The configuration values include host binding, port, TLS certificate file, and TLS key file.
"""

from project.config.server import host_binding, port
from project.config.tls import tls_certfile, tls_keyfile

__all__ = ["host_binding", "port", "tls_certfile", "tls_keyfile"]
