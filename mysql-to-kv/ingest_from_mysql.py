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
import pymysql
import requests
import json
import pandas as pd
from requests.auth import HTTPBasicAuth


def _pack_putitem_body(key, row):
    """
    PutItem request body formater
    """
    dict_item = dict()
    for k, v in row.iteritems():
        dict_item[k] = {'N' if isinstance(v, int) else 'S': '{}'.format(v)}
    body = {
            "Key": {
                "ID": {
                    "N": '{}'.format(key)
                }
            },
            "Item": dict_item
        }
    return body


def _putitem(url, body, user, password):
    """
    PutItem request
    """
    headers = {'Content-Type': 'application/json', 'X-v3io-function': 'PutItem'}
    res = requests.post(url=url, data=json.dumps(body), headers=headers, auth=HTTPBasicAuth(user, password))
    return res


def handler(context, event):
    #################
    # IGZ variables #
    #################
    # table
    table = os.getenv('TABLE', 'table')
    # bigdata
    container = os.getenv('CONTAINER', 'bigdata')
    # iguazio user
    igz_user = os.getenv('IGZ_USER', 'iguazio')
    # iguazio password
    igz_password = os.getenv('IGZ_PWD', 'dIusluqnAoJl5wNV')

    ###################
    # MYSQL variables #
    ###################
    # mysql-rfam-public.ebi.ac.uk
    host = os.getenv('SQL_HOST', 'mysql-rfam-public.ebi.ac.uk')
    # 4497
    port = os.getenv('SQL_PORT', 4497)
    # rfamro
    user = os.getenv('SQL_USER', 'rfamro')
    # <empty string>
    password = ''
    # Rfam
    database = os.getenv('SQL_DB_NAME', 'Rfam')

    conn = pymysql.connect(
        host=host,
        port=int(port),
        user=user,
        passwd=password,
        db=database,
        charset='utf8mb4')
    df = pd.read_sql_query('select rfam_acc,rfam_id,auto_wiki,description,author,seed_source FROM family LIMIT 10', conn)
    for index, row in df.iterrows():
        body = _pack_putitem_body(index, row)
        try:
            res = _putitem(f'http://v3io-webapi:8081/{container}/{table}/', body, igz_user, igz_password)

        except Exception:
            context.logger.warn("Failed to send request")
            return context.Response(body='An issue was occured',
                                headers={},
                                content_type='text/plain',
                                status_code=500)

    return context.Response(body='PutItem completed successfully',
                        headers={},
                        content_type='text/plain',
                        status_code=200)
