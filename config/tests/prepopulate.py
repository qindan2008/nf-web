import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from . import data, utils, queries as q


def oddjob_db_engine():
    return create_engine(os.getenv('ODDJOB_DB_URL'))


def flows_db_engine():
    return create_engine(os.getenv('FLOWS_DB_URL'))


def processing_db_engine():
    return create_engine(os.getenv('PROCESSING_DB_URL'))


def setup_services(oddjob_db_engine, flows_db_engine, processing_db_engine):
    # Register wr runner on OddJob
    with oddjob_db_engine.begin() as conn:
        try:
            q.insert_runner(conn, data.NF_RUNNER)
        except IntegrityError as ex:
            logging.warning(ex.orig)

    with flows_db_engine.begin() as conn:
        try:
            for component in data.COMPONENTS.keys():
                q.insert_component(conn, utils.get_component(component))
        except IntegrityError as ex:
            logging.warning(ex.orig)


oj = oddjob_db_engine()
fl = flows_db_engine()
pr = processing_db_engine()
setup_services(oj, fl, pr)


