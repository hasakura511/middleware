from datetime import datetime as dt
from fastapi.requests import Request

import inspect


def product_logger(tag=None, message='', request: Request = None):
    # print(inspect.stack()[0][3])  #log
    # print(inspect.stack()[1][3])  #caller of log
    stack = inspect.stack()
    func_name = f"{stack[1][1].split('/')[-1]}:{stack[1][3]}"
    timestamp = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    if tag is None and request:
        tag = request.url

    # w+ rewrite file each time "a+" appends
    with open('log.txt', 'w+') as logfile:
        line = f'{timestamp}: {func_name}: {tag}: {message}\n'
        print(line, flush=True)
        logfile.write(line)
