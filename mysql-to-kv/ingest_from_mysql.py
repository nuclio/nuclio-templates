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
import pandas as pd
import v3io_frames as v3f

def handler(context, event):
    sql_query = os.getenv('SQL_QUERY')
    df = pd.read_sql_query(sql_query, context.dbconn)
    context.client.write(backend='kv', table=os.getenv('TABLE'), dfs=df)

def init_context(context):
    # IGZ variables
    container = os.getenv('CONTAINER')
    igz_v3f = os.getenv('IGZ_V3F')
    igz_v3f_port = os.getenv('IGZ_V3F_PORT')

    # MYSQL variables
    host = os.getenv('SQL_HOST')
    port = os.getenv('SQL_PORT')
    user = os.getenv('SQL_USER')
    password = os.getenv('SQL_PWD', "")
    database = os.getenv('SQL_DB_NAME')

    # Init v3io-frames connection and set it as a context attribute
    client = v3f.Client(address=f'{igz_v3f}:{igz_v3f_port}', password=os.getenv('IGZ_PWD'), container=container)
    setattr(context, 'client', client)

    # Init DB connection and set it as a context attribute
    dbconn = pymysql.connect(
        host=host,
        port=int(port),
        user=user,
        passwd=password,
        db=database,
        charset='utf8mb4')
    setattr(context, 'dbconn', dbconn)
