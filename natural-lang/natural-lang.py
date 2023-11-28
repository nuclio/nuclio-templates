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
from textblob import TextBlob
import os


def handler(context, event):
    context.logger.info('This is an NLP example!')

    # process and correct the text
    blob = TextBlob(str(event.body))
    corrected = blob.correct()

    # debug print the text before and after correction
    context.logger.debug_with("Corrected text", corrected=str(corrected), orig=str(blob))

    # calculate sentiments
    context.logger.info_with("Sentiment",
                             polarity=str(corrected.sentiment.polarity),
                             subjectivity=str(corrected.sentiment.subjectivity))

    # read target language from environment and return translated text
    lang = os.getenv('TO_LANG', 'fr')
    return str(corrected.translate(to=lang))
