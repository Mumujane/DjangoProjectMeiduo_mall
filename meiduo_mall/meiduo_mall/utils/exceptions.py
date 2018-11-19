import logging

from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from django.db import DatabaseError
from redis.exceptions import RedisError

# 获取Django日志器
logger = logging.getLogger("django")

def exception_handler(exc, context):
    """

    :param exc: 异常对象
    :param context: 异常上下文
    :return:

    """

    # 1. drf 处理异常
    # 2. 自己处理异常
    response = drf_exception_handler(exc, context)

    if not response:
        logging.error('[%s] %s' % (context['view'], exc))
        if isinstance(exc, (DatabaseError, RedisError)):
            return Response({'error': '服务器内部异常'}, status=507)

    return response
