"""Reload the DB in DEV mode."""

from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path
from re import match
from string import Template
from typing import Final

from loguru import logger
from sqlalchemy import Connection, create_engine, text

from library.config.config import resources_path
from library.config.db import (
    db_connect_args,
    db_dialect,
    db_log_statements,
    db_url_admin,
)
from library.config.dev_mode import dev_db_populate
from library.repository import engine

__all__ = ["DbPopulateService", "db_populate", "get_db_populate_service"]


utf8: Final = "utf-8"
_db_traversable: Final[Traversable] = files(resources_path)


class DbPopulateService:
    """Reload the DB in DEV mode by executing SQL statements from files and loading CSV files."""

    def __init__(self) -> None:
        """Initialize the DbPopulateService with a database engine for administrative tasks."""
        self.engine_admin: Final = (
            create_engine(
                db_url_admin,
                connect_args=db_connect_args,
                echo=db_log_statements,
            )
            if db_dialect == "postgresql"
            else create_engine(db_url_admin, echo=db_log_statements)
        )

    def populate(self) -> None:
        """Reload the DB by executing SQL statements from files and loading CSV files, if in DEV mode."""
        if not dev_db_populate:
            return

        logger.warning(">>> The DB is reloading: {} <<<", engine.url)
        connection: Connection
        with engine.connect() as connection:
            db_dialect: Final = connection.dialect.name
            dialect_path: Final = _db_traversable / db_dialect
            with Path(str(dialect_path / "drop.sql")).open(encoding=utf8) as drop_sql:
                zeilen_drop: Final = self._remove_comment(drop_sql.readlines())
                drop_statements: Final = self._build_sql_statements(zeilen_drop)
                for stmt in drop_statements:
                    connection.execute(text(stmt))
            with Path(str(dialect_path / "create.sql")).open(encoding=utf8) as create_sql:
                zeilen_create: Final = self._remove_comment(create_sql.readlines())
                create_statements: Final = self._build_sql_statements(zeilen_create)
                for stmt in create_statements:
                    connection.execute(text(stmt))
            connection.commit()
        engine.dispose()
        self._load_csv_files()
        logger.warning(">>> The DB is up to date! <<<")

    def _remove_comment(self, zeilen: list[str]) -> list[str]:
        """Remove SQL-comments and spaces."""
        return [zeile for zeile in zeilen if not match(r"^ *--", zeile) and zeile != "\n"]

    def _build_sql_statements(self, zeilen: list[str]) -> list[str]:
        """Wrap all SQL-statements into one line."""
        statements: list[str] = []
        sql: str = ""
        anzahl: Final = len(zeilen)
        for i in range(anzahl):
            zeile = zeilen[i]
            sql += zeile.replace("\n", " ")
            if zeile.endswith(";\n"):
                statements.append(sql)
                sql = ""
        return statements

    def _load_csv_files(self) -> None:
        logger.debug("begin")
        tabellen: Final = ["member", "address", "book"]
        csv_path: Final = "/init/library/csv"
        with self.engine_admin.connect() as connection:
            connection.execute(text("SET search_path TO library;"))
            for tabelle in tabellen:
                self._load_csv_file(
                    tabelle=tabelle,
                    csv_path=csv_path,
                    connection=connection,
                )
                connection.commit()
        self.engine_admin.dispose()

    def _load_csv_file(self, tabelle: str, csv_path: str, connection: Connection) -> None:
        logger.debug("table={}", tabelle)
        copy_cmd: Final = Template(
            "COPY ${TABELLE} FROM '" + csv_path + "/${TABELLE}.csv' (FORMAT csv, QUOTE '\"', DELIMITER ';', HEADER true);",
        ).substitute(TABELLE=tabelle)
        connection.execute(text(copy_cmd))


def get_db_populate_service() -> DbPopulateService:
    """Factory-Function for DbPopulateService."""
    return DbPopulateService()


def db_populate():
    """Reload the DB in DEV mode by executing SQL statements from files and loading CSV files, if in DEV mode."""
    if dev_db_populate:
        service = get_db_populate_service()
        service.populate()
