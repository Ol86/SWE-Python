"""Asynchronous session factory for the database."""

from typing import Final

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from library.config.db import db_connect_args, db_log_statements, db_url

__all__ = ["Session", "engine"]

engine: Final = create_engine(
    db_url,
    connect_args=db_connect_args,
    echo=db_log_statements,
)
logger.info("Database engine created")

Session: sessionmaker = sessionmaker(bind=engine, autoflush=False)
logger.info("Session factory created")
