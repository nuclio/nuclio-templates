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

import nuclio_sdk
import json

INGEST_FUNCTION = os.environ['INGEST_FUNCTION']


# Example tsdb event:
#
# {
# 		"metric": "cpu",
# 		"labels": {
# 			"dc": "7",
# 			"hostname": "mybesthost"
# 		},
# 		"samples": [
# 			{
# 				"t": "1532595945142",
# 				"v": {
# 					"N": 95.2
# 				}
# 			},
# 			{
# 				"t": "1532595948517",
# 				"v": {
# 					"n": 86.8
# 				}
# 			}
# 		]
# }


# transform kafka event to tsdb event
def transform_to_tsdb_event(event):

    # implement the transformation
    return event


def handler(context, event):

    # parse the given event body
    event_body = json.loads(event.body)

    tsdb_event = transform_to_tsdb_event(event_body)

    # ingest the parsed event to tsdb
    context.platform.call_function(INGEST_FUNCTION, nuclio_sdk.Event(body=tsdb_event))
