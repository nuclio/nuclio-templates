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
