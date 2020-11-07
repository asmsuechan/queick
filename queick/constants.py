def enum(name, *sequential, **named):
    values = dict(zip(sequential, range(len(sequential))), **named)
    return type(str(name), (), values)


RETRY_TYPE = enum(
    'RetryType',
    CONSTANT='constant',
    LINEAR_INCREASING='linear_increasing',
    COUNT_INCREASING='count_increasing',
    EXPONENTIAL='exponential',
)

NW_STATE = enum(
    'State',
    CONNECTED='connected',
    DISCONNECTED='disconnected',
    INITIATED='initiated',
)

TCP_SERVER_HOST = '127.0.0.1'
TCP_SERVER_PORT = 9999
