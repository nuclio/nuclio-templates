from textblob import TextBlob
import os


def handler(context, event):
    context.logger.info('This is an NLP example! ')

    # process and correct the text
    blob = TextBlob(str(event.body))
    corrected = blob.correct()

    # debug print the text before and after correction
    context.logger.debug_with("corrected text", corrected=str(corrected), orig=str(blob))

    # calculate sentiments
    context.logger.info_with("sentiment",
                             polarity=str(corrected.sentiment.polarity),
                             subjectivity=str(corrected.sentiment.subjectivity))

    # read target language from environment and return translated text
    lang = os.getenv('TO_LANG')
    return str(corrected.translate(to=lang))
