import json
import os



NF_RUNNER = {
    'id': 1,
    'external_id': '0603b671-2186-41cd-b6ed-c686ae51d67b',
    'type': 'nf',
    'name': 'nf-0',
    'status': 'ACCEPTING_SUBMISSIONS',
    'url': os.getenv('NF_SERVER_HOST'),
    'credentials': json.dumps({
        'token': os.getenv('NF_AUTH_TOKEN'),
    })
}

COMPONENTS = {
    'nf-basic': {
        'id': 1,
        'external_id': '0603b671-2186-41cd-b6ed-c686ae51d67b'
    }
}
