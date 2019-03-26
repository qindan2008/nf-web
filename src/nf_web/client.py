import logging
import os
from http import HTTPStatus
from typing import List

import requests
import yaml
from bravado.client import SwaggerClient


def get_client(url):
    with open(os.getenv("SWAGGER_SCHEMA",
                        os.path.join(os.path.dirname(__file__), "swagger.yml"))) as f:
        spec = yaml.load(f)
    client = SwaggerClient.from_spec(spec)
    client.swagger_spec.api_url = url
    return client


class ProcessingClient:

    def __init__(self, base_url):
        self.base_url = base_url

    def ping(self):
        return requests.get(f"{self.base_url}/ping")

    def get_components(self):
        return requests.get(f"{self.base_url}/components", params={"info": True}).json()

    def get_component(self, component_id):
        return requests.get(f"{self.base_url}/components/{component_id}").json()

    def post_components_groups(self, component_id, group_id, params):
        print(f"Params: {params}")
        return requests.post(
            f"{self.base_url}/components/{component_id}/groups",
            json={
                'group_id': group_id,
                'params': params
            })

    def get_jobs(self, status=None):
        params = {'status': status} if status else None
        return requests.get(f"{self.base_url}/jobs", params=params).json()

    def put_triggers_jobs_check(self):
        return requests.put(f"{self.base_url}/triggers/jobs/check")


class OddJobClient:

    def __init__(self, base_url):
        self.base_url = base_url

    def ping(self):
        return requests.get(f"{self.base_url}/ping")

    def trigger_task(self, path: str) -> None:
        response = requests.put(
            f"{self.base_url}/{path}",
            json={
                "per_batch_jobs": 5,
                "max_jobs": 10,
                "timeout": 5
            })
        assert response.status_code == HTTPStatus.OK

    def trigger_task_job_submit(self) -> None:
        self.trigger_task('/triggers/jobs/submit')

    def trigger_task_job_check(self) -> None:
        self.trigger_task('/triggers/jobs/check')

    def check_job(self, job_ids: List[str]):
        return requests.get(f"{self.base_url}/jobs", json={"ids": [job_id for job_id in job_ids]}).json()['found']
