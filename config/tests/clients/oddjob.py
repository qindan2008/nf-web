import os
from http import HTTPStatus

import requests


BASE_URL = os.getenv('ODDJOB_URL')


def ping():
    return requests.get(f"{BASE_URL}/ping")


def trigger_task(path: str) -> None:
    response = requests.put(
        f"{BASE_URL}/{path}",
        json={
            "per_batch_jobs": 5,
            "max_jobs": 10,
            "timeout": 5
        })
    assert response.status_code == HTTPStatus.OK


def trigger_task_job_submit() -> None:
    trigger_task('/triggers/jobs/submit')


def trigger_task_job_check() -> None:
    trigger_task('/triggers/jobs/check')
