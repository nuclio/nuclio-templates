# Copyright 2019 The Nuclio Authors.
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

import requests
import json
import base64
import os


def init_context(context):
    # env -> config
    setattr(context.user_data, 'config', {
        'v3io_api': os.environ['V3IO_API'],
        'v3io_username': os.environ['V3IO_USERNAME'],
        'container_name': os.environ['CONTAINER_NAME'],
        'table_name': os.environ['TABLE_NAME'],
        'input_stream_search_key': os.environ['INPUT_STREAM_SEARCH_KEY'],
        'output_stream_name': os.environ['OUTPUT_STREAM_NAME'],
        'v3io_access_key': os.environ['V3IO_ACCESS_KEY'],
    })


def handler(context, event):
    config = context.user_data.config
    msg = json.loads(event.body)
    context.logger.info(f'Incoming message: {msg}')
    enrichment_data = _search_kv(msg, config)
    context.logger.info(f'Enrichment data: {enrichment_data}')
    msg['enrichment'] = enrichment_data
    _put_records([msg], config)
    context.logger.debug(f'Output message: {msg}')


def _get_url(v3io_api, container_name, collection_path):
    return f'http://{v3io_api}/{container_name}/{collection_path}'


def _get_headers(v3io_function, v3io_access_key):
    return {
        'Content-Type': "application/json",
        'X-v3io-function': v3io_function,
        'cache-control': "no-cache",
        'x-v3io-session-key': v3io_access_key
    }


def _search_kv(msg, config):
    v3io_api = config['v3io_api']
    v3io_username = config['v3io_username']
    container_name = config['container_name']
    search_value = msg[config['input_stream_search_key']]
    table_path_and_key = f"{v3io_username}/examples/stream-enrich/{config['table_name']}/{search_value}"
    v3io_access_key = config['v3io_access_key']

    url = _get_url(v3io_api, container_name, table_path_and_key)
    headers = _get_headers("GetItem", v3io_access_key)
    resp = requests.request("POST", url, json={}, headers=headers)

    json_response = json.loads(resp.text)

    response = {}
    if 'Item' in json_response:
        response = json_response['Item']

    return response


def _put_records(items, config):
    v3io_api = config['v3io_api']
    v3io_username = config['v3io_username']
    container_name = config['container_name']
    output_stream_path = f"{v3io_username}/examples/stream-enrich/{config['output_stream_name']}/"
    v3io_access_key = config['v3io_access_key']

    records = _items_to_records(items)
    url = _get_url(v3io_api, container_name, output_stream_path)
    headers = _get_headers("PutRecords", v3io_access_key)

    return requests.request("PUT", url, json=records, headers=headers)


def _item_to_b64(item):
    item_string = json.dumps(item)
    return base64.b64encode(item_string.encode('utf-8')).decode('utf-8')


def _items_to_records(items):
    return {'Records': [{'Data': _item_to_b64(item)} for item in items]}
