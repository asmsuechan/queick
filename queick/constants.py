def enum(name, *sequential, **named):
    values = dict(zip(sequential, range(len(sequential))), **named)
    return type(str(name), (), values)

RETRY_TYPE = enum(
    'RetryType',
    CONSTANT='constant',
    LINEAR_INCREASING='linear_increasing',
    COUNT_INCREASING='count_increasing',
)
