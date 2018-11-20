from django.shortcuts import render

from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView
from celery_tasks.sms import tasks as sms_tasks

import random
# Create your views here.
class SMSCodeView(APIView):
    def get(self, request, mobile):
        """
        1. 校验短信是否发送过
        2. 如果已经发送,返回已发送信息
        3. 生成随机验证码
        4. 保存验证码到reids 中, sms_{mobile}
        5. 保存已发送状态 smsflag_{mobile}
        6. 给用户手机发短信
        7. 返回客户端 发送成功
        :param request:
        :param mobile:
        :return:
        """
        redis_conn = get_redis_connection("verifications")
        send_flag = redis_conn.get("send_flag_%s" %mobile)
        if send_flag:
            return Response({"message": "短信发送频繁"}, status = 400)
        sms_code = random.randint(10000, 99999)

        # # def setex(self, name, value, time):
        # redis_conn.setex("sms_%s" %mobile, 5*60, sms_code) # 直接和redis进行交互
        #
        # # 保存发送状态
        # redis_conn.setex("smsflag_%s" % mobile, 60 ,1)

        # 获取管道对象
        pl = redis_conn.pipline()
        pl.setex('sms_%s' % mobile, 5*60, sms_code)
        pl.setex('smsflag_%s' % mobile, 60, 1)

        # 执行管道中所有命令
        pl.execute()

        # 发送短信给用户手机
        # CCP().send_template_sms(mobile)

        sms_code_expires = constants.SMS_CODE_REDIS_EXPIRE // 60

        sms_tasks.delay(mobile, sms_code, sms_code_expires)


        return Response({'message': 'OK'})










