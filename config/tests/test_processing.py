from time import sleep

import pytest
from . import utils
from .clients import processing, oddjob
from sqlalchemy import text

SELECT_COMP_GROUPS = text("""
select
    c.id,
    c.external_id,
    c.component_id,
    c.group_id,
    c.added_on,
    s.name as status,
    c.params
from comp_groups c
left join statuses s on s.id = c.status_id
""")


def get_all_comp_groups(engine):
    with engine.begin() as conn:
        return conn.execute(SELECT_COMP_GROUPS)


def test_ping():
    assert processing.ping().status_code == 204


def test_get_components():
    r = processing.get_components()
    payload = r.json()

    assert r.status_code == 200

    for comp in payload:
        print(comp)


@pytest.mark.parametrize('component_name', ['nf-basic'])
def test_get_component(component_name):
    component_id = utils.get_component_id(component_name)
    r = processing.get_component(component_id)
    assert r.status_code == 200
    payload = r.json()
    assert 'id' in payload
    assert 'parameters' in payload

@pytest.mark.parametrize('component_name,params', [
    ('nf-basic', {
        'fasta_file': '>gi|186681228|ref|YP_001864424.1| phycoerythrobilin:ferredoxin oxidoreductase'
                      'MNSERSDVTLYQPFLDYAIAYMRSRLDLEPYPIPTGFESNSAVVGKGKNQEEVVTTSYAFQTAKLRQIRA'
                      'AHVQGGNSLQVLNFVIFPHLNYDLPFFGADLVTLPGGHLIALDMQPLFRDDSAYQAKYTEPILPIFHAHQ'
                      'QHLSWGGDFPEEAQPFFSPAFLWTRPQETAVVETQVFAAFKDYLKAYLDFVEQAEAVTDSQNLVAIKQAQ'
                      'LRYLRYRAEKDPARGMFKRFYGAEWTEEYIHGFLFDLERKLTVVK'
    }
     )
])
def test_post_components_groups(component_name, params):
    component_id = utils.get_component_id(component_name)
    r = processing.post_components_groups(component_id, '', params)
    assert r.status_code == 200


def test_check_jobs(processing_db_engine):
    r = processing.put_triggers_jobs_check()
    assert r.status_code == 202

    cgs = get_all_comp_groups(processing_db_engine)
    assert all(cg.status == 'pending' for cg in cgs)


def _test_get_jobs_payload(payload):
    assert isinstance(payload, list)
    assert all(
        'id' in job and 'job_id' in job and 'status' in job
        for job in payload)
    assert all(job.values() for job in payload)


def test_get_jobs():
    r = processing.get_jobs()
    assert r.status_code == 200
    payload = r.json()
    _test_get_jobs_payload(payload)


@pytest.mark.parametrize('job_status', ['pending', 'failed'])
def test_get_jobs_by_status(job_status):
    r = processing.get_jobs(status=job_status)
    assert r.status_code == 200
    payload = r.json()
    _test_get_jobs_payload(payload)
    assert all(job['status'] == job_status for job in payload)


@pytest.mark.parametrize('component_name,params', [
    # ('cgpmap', {
    #     'mm_duplicate_qc': False,
    #     'filename': 'readgroupfile1.fq.gz',
    #     'sample': f'S1-{uuid.uuid4()}'
    # }),
    ('nf-basic', {
        'fasta_file': '>gi|186681228|ref|YP_001864424.1| phycoerythrobilin:ferredoxin oxidoreductase'
                      'MNSERSDVTLYQPFLDYAIAYYRSRLDLEPYPIPTGFESNSAVVGKGKNQEEVVTTSYAFQTAKLRQIRA'
                      'AHVQGGNSLQVLNFVIFPHLNYDLPFFGADLVTLPGGHLIALDMQPLFRDDSAYQAKYTEPILPIFHAHQ'
                      'QHLSWGGDFPEEAQPFFSPAFLWTRPQETAVVETQVFAAFKDYLKAYLDFVEQAEAVTDSQNLVAIKQAQ'
                      'LRYLRYRAEKDPARGMFKRFYGAEWTEEYIHGFLFDLERKLTVVK'
    }
     )
])
def test_run_pipeline(component_name, params, processing_db_engine):
    component_id = utils.get_component_id(component_name)
    r = processing.post_components_groups(component_id, '', params)
    assert r.status_code == 200
    r = processing.put_triggers_jobs_check()
    assert r.status_code == 202
    cgs = get_all_comp_groups(processing_db_engine)
    assert all(cg.status == 'pending' for cg in cgs)
    oddjob.trigger_task_job_submit()
    sleep(15)
    oddjob.trigger_task_job_check()
    sleep(1)
    # cgs = get_all_comp_groups(processing_db_engine)
    # assert all(cg.status == 'running' for cg in cgs)
    # oddjob.trigger_task_job_check()
    processing.put_triggers_jobs_check()
    sleep(1)
    cgs = get_all_comp_groups(processing_db_engine)
    assert all(cg.status == 'completed' for cg in cgs)
    cgs = get_all_comp_groups(processing_db_engine)
    for cg in cgs:
        print(cg.status)