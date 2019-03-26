import os
import requests


BASE_URL = os.getenv('PROCESSING_URL')


def ping():
    return requests.get(f"{BASE_URL}/ping")


def get_components():
    return requests.get(f"{BASE_URL}/components")


def get_component(component_id):
    return requests.get(f"{BASE_URL}/components/{component_id}")


def post_components_groups(component_id, group_id, params):
    return requests.post(
        f"{BASE_URL}/components/{component_id}/groups",
        json={
            'group_id': group_id,
            'params': params
        })


def get_jobs(status=None):
    params = {'status': status} if status else None
    return requests.get(f"{BASE_URL}/jobs", params=params)


def put_triggers_jobs_check():
    return requests.put(f"{BASE_URL}/triggers/jobs/check")
