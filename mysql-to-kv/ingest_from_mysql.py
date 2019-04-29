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

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import v3io_frames as v3f

# MYSQL db variables
SQL_QUERY = os.environ['SQL_QUERY']
SQL_HOST = os.environ['SQL_HOST']
SQL_PORT = os.environ['SQL_PORT']
SQL_USER = os.environ['SQL_USER']
SQL_PWD = os.getenv('SQL_PWD', '')
SQL_DB_NAME = os.environ['SQL_DB_NAME']

# Iguazio platform variables
IGZ_V3F = os.environ['IGZ_V3F']
IGZ_USER = os.environ['IGZ_USER']
IGZ_PWD = os.environ['IGZ_PWD']
CONTAINER = os.environ['CONTAINER']


def handler(context, event):
    df = pd.read_sql_query(SQL_QUERY, context.dbconn.connection())

    # for debugging the generated my-sql query
    context.logger.debug_with('df count', no_of_records=df.shape[0])
    context.client.write(backend='kv', table=os.getenv('TABLE'), dfs=df)


def init_context(context):
    # Init v3io-frames connection and set it as a context attribute
    client = v3f.Client(address=IGZ_V3F,
                        user=IGZ_USER,
                        password=IGZ_PWD,
                        container=CONTAINER)
    setattr(context, 'client', client)

    connection_string = f"mysql://{SQL_USER}:{SQL_PWD}@{SQL_HOST}:{SQL_PORT}/{SQL_DB_NAME}"
    engine = create_engine(connection_string, encoding='utf8', convert_unicode=True, isolation_level='READ_COMMITTED')
    session = sessionmaker()
    session.configure(bind=engine)
    dbconn = session()
    setattr(context, 'dbconn', dbconn)
