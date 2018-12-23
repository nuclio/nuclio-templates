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


def handler(context, event):
    injest_function = os.environ['INJEST_FUNCTION']

    # parse the given event body
    event_body = json.loads(event.body)

    # ingest the parsed event to tsdb
    context.platform.call_function(injest_function, nuclio_sdk.Event(body=event_body))
