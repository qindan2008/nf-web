import json
import yaml
import os
from . import data


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def get_component(component_name):
    with open(get_abs_path(f"components/{component_name}.yml")) as fh:
        raw_config = fh.read()

    config = yaml.load(raw_config)

    return {
        'name': config['name'],
        'version': config['version'],
        'raw_config': raw_config,
        'config': json.dumps(config),
        **data.COMPONENTS[component_name]
    }


def get_component_id(component_name):
    return data.COMPONENTS[component_name]['external_id']


def delete_all(conn, table_names):
    for table_name in table_names:
        conn.execute(f"delete from {table_name}")


def select_all(conn, table_name):
    return list(conn.execute(f"select * from {table_name}"))


def clean_tables(engine, tables):
    with engine.begin() as conn:
        delete_all(conn, tables)
