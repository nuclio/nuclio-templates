# Copyright 2017 The Nuclio Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import json

import requests

V3IO_API_ENDPOINT_HOST = os.environ['V3IO_API_ENDPOINT_HOST']
V3IO_API_ENDPOINT_PORT = os.environ['V3IO_API_ENDPOINT_PORT']
TABLE_NAME = os.environ['TABLE_NAME']
CONTAINER_NAME = os.environ['CONTAINER_NAME']
EVENT_KEY = os.environ['EVENT_KEY']
USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']


def handler(context, event):
    payload = _generate_payload(event.body)
    url = _get_request_url()
    headers = _get_request_headers('PutItem')
    auth = requests.auth.HTTPBasicAuth(USERNAME, PASSWORD)

    _send_request(payload, context.logger, url, headers, auth)


def _get_request_url():
    return f'http://{V3IO_API_ENDPOINT_HOST}:{V3IO_API_ENDPOINT_PORT}/{CONTAINER_NAME}/{TABLE_NAME}/'


def _get_request_headers(v3io_function):
    return {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'X-v3io-function': v3io_function,
    }


def _send_request(payload, logger, url, headers, auth):
    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth, timeout=1)
        logger.debug(response.status_code)
        logger.debug(response.content)
    except Exception as e:
        logger.error('ERROR: {0}'.format(str(e)))


def _insert_key(key):
    item = {}
    item['Key'] = {'name': {'S': key}}
    return item


def _insert_attributes(item, attributes, allow_null_attributes=True):
    if attributes:
        item['Item'] = {}
        for attr, definition in attributes.items():
            item['Item'][attr] = {}
            for key, value in definition.items():
                if allow_null_attributes or value is not None:
                    item['Item'][attr][key] = value
            if not item['Item'][attr]:
                item['Item'].pop(attr)
    return item


def _generate_attributes(json_object, object_key):
    attributes = {}
    for key in json_object:
        object_type = type(json_object[key])
        if key != object_key:
            if object_type is bool:
                attributes[key] = {'BOOL': json_object[key]}
            elif object_type is int:
                attributes[key] = {'N': str(json_object[key])}
            elif object_type is float:
                attributes[key] = {'N': str(json_object[key])}
            elif object_type is str:
                attributes[key] = {'S': json_object[key]}
    return attributes


def _generate_payload(event_body):
    msg = json.loads(event_body)
    attributes = _generate_attributes(msg, EVENT_KEY)
    payload = _insert_key(msg[EVENT_KEY])
    return _insert_attributes(payload, attributes)
