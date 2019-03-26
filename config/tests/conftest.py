import logging
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from . import data, utils, queries as q


@pytest.fixture(scope='session', autouse=True)
def oddjob_db_engine():
    return create_engine(os.getenv('ODDJOB_DB_URL'))


@pytest.fixture(scope='session', autouse=True)
def flows_db_engine():
    return create_engine(os.getenv('FLOWS_DB_URL'))


@pytest.fixture(scope='session', autouse=True)
def processing_db_engine():
    return create_engine(os.getenv('PROCESSING_DB_URL'))


@pytest.fixture(scope='session', autouse=True)
def setup_services(oddjob_db_engine, flows_db_engine, processing_db_engine):
    # Register wr runner on OddJob
    with oddjob_db_engine.begin() as conn:
        try:
            q.insert_runner(conn, data.WR_RUNNER)
            q.insert_runner(conn, data.NF_RUNNER)
        except IntegrityError as ex:
            logging.warning(ex.orig)

    # Register cgpMap component on Flows
    with flows_db_engine.begin() as conn:
        try:
            for component in data.COMPONENTS.keys():
                q.insert_component(conn, utils.get_component(component))
        except IntegrityError as ex:
            logging.warning(ex.orig)


    # utils.clean_tables(processing_db_engine, ['comp_groups'])
    # utils.clean_tables(oddjob_db_engine, [
    #     'job_error_info',
    #     'job_history',
    #     'jobs',
    #     'runners'
    # ])
