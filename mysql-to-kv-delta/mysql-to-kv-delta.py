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
import time
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import v3io_frames as v3f


TABLE = os.getenv('TABLE')
DELTA_INTERVAL_MINUTE = os.getenv('DELTA_INTERVAL_MINUTE')
MODIFIED_DATETIME_COL = os.getenv('MODIFIED_DATETIME_COL')
CREATED_DATETIME_COL = os.getenv('CREATED_DATETIME_COL')


def handler(context, event):
    datetime_query = str(datetime.datetime.now() - datetime.timedelta(seconds=int(DELTA_INTERVAL_MINUTE)*60))
    sql_query = os.getenv('SQL_QUERY')
    sql_query_diff = '{0} where ({1}>=\'{2}\' AND {3} IS NULL) OR ({4}>=\'{5}\')'.format(sql_query, CREATED_DATETIME_COL, str(datetime_query), MODIFIED_DATETIME_COL, MODIFIED_DATETIME_COL, str(datetime_query))
    context.logger.debug(sql_query_diff)
    df = pd.read_sql(sql_query_diff, context.dbconn.connection())
    context.logger.debug('no of delta rows :: {} '.format(df.shape[0]))
    context.client.write(backend='kv', table=TABLE, dfs=df)


def init_context(context):

    # MYSQL variables
    host = os.getenv('SQL_HOST')
    port = os.getenv('SQL_PORT')
    user = os.getenv('SQL_USER')
    password = os.getenv('SQL_PWD', '')
    database = os.getenv('SQL_DB_NAME')

    # Init v3io-frames connection and set it as a context attribute
    client = v3f.Client(address=os.getenv('IGZ_V3F'), username=os.getenv('IGZ_USER'),password=os.getenv('IGZ_PWD'), container=os.getenv('CONTAINER'))
    setattr(context, 'client', client)

    connection_string = 'mysql://{0}:{1}@{2}:{3}/{4}'.format(user, password, host, port, database)
    engine = create_engine(connection_string, encoding='utf8', convert_unicode=True,
    isolation_level='READ_COMMITTED')
    session = sessionmaker()
    session.configure(bind=engine)
    dbconn = session()
    setattr(context, 'dbconn', dbconn)
