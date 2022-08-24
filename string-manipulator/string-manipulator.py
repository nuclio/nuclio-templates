# Copyright 2018 The Nuclio Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import hashlib

def handler(context, event):
    manipulation_kind = os.environ['MANIPULATION_KIND']

    manipulators_by_kind = {
        'reverse': _reverse_string,
        'md5': _md5_string
    }
    
    # get manipulator, default to echo
    manipulator = manipulators_by_kind.get(manipulation_kind, _echo)
     
    # call it, passing the body and returning the value
    return manipulator(event.body)


def _echo(value):
    return value


def _reverse_string(value):
    return value[::-1]


def _md5_string(value):
    encoder = hashlib.md5()
    encoder.update(value)
    return encoder.hexdigest()
