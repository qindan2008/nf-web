from sqlalchemy import text


OJ_INSERT_RUNNER = text("""
insert into runners (id, name, external_id, url, credentials, type, status)
values (
    :id,
    :name,
    :external_id,
    :url,
    :credentials,
    (select rt.id from runner_types_dict rt where name = :type),
    (select rs.id from runner_states_dict rs where name = :status)
)
""")


FLOWS_INSERT_COMP = text("""
insert into components (id, external_id, name, version, raw_config, config)
values (:id, :external_id, :name, :version, :raw_config, :config)
""")


def insert_runner(conn, runner):
    conn.execute(OJ_INSERT_RUNNER, **runner)


def insert_component(conn, comp):
    conn.execute(FLOWS_INSERT_COMP, **comp)
