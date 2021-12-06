from pathlib import Path
from app import log


def chunks(l, chunk_size):
    """
    Yield successive n-sized chunks from l which is a generator
    """
    result = []
    for elem in l:
        if len(result) < chunk_size:
            result.append(elem)
        else:
            yield result
            result = [elem]
    yield result
    result = []


def errors_to_desc(errors):
    msg = []

    for k in errors:
        if isinstance(errors[k][0], str):
            msg.append('\"{}\": {}'.format(k, ';'.join(errors[k])))
        else:
            inner_message = ''
            for inner_errors in errors[k]:
                inner_message += errors_to_desc(inner_errors)
            msg.append('\"{}\": {}'.format(k, inner_message))

    return '. '.join(msg)


LOG = log.get_logger()