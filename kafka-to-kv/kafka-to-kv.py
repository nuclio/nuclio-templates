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
import base64

import requests

def get_request_url(nginx_host, nginx_port, container_id, table_name):

    # assumes default container (id=1)
    return 'http://{0}:{1}/{2}/{3}'.format(nginx_host, nginx_port, container_id, table_name)


def get_request_headers(v3io_function, username, password):
    encoded_auth = base64.b64encode('{0}:{1}'.format(username, password))
    return {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'X-v3io-function': v3io_function,
        'Authorization': 'Basic {0}'.format(encoded_auth),
    }


def send_request(payload, logger, url, headers):

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=1)
        logger.info(response.status_code)
        logger.info(response.content)
    except Exception as e:
        logger.info("ERROR: {0}".format(str(e)))


def insert_key(item,key):
    item['Key'] = {"name": {"S": key}}
    return item


def insert_attributes(item, attributes, allow_null_attributes=True):
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


def generate_attributes(json_object, object_key):
    attributes = {}
    for key in json_object:
        if key != object_key:
            if type(json_object[key]) == int:
                attributes[key] = {"N": json_object[key]}
            if type(json_object[key]) == float:
                attributes[key] = {"N": json_object[key]}
            if type(json_object[key]) == str:
                attributes[key] = {"S": json_object[key]}
    return attributes


def generate_payload(event_body, key):
    msg = json.loads(event_body)
    attributes = generate_attributes(msg, key)
    payload = {}
    payload = insert_key(payload, msg[key])
    payload = insert_attributes(payload, attributes)
    return payload


def handler(context, event):
    nginx_host = os.environ['NGINX_HOST']
    nginx_port = os.environ['NGINX_PORT']
    table_name = os.environ['TABLE_NAME']
    container_id = os.environ['CONTAINER_ID']
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']

    payload = generate_payload(event.body,"key")
    url = get_request_url(nginx_host, nginx_port, table_name, container_id)
    headers = get_request_headers('PutItem', username, password)

    send_request(payload, context.logger, url, headers)
