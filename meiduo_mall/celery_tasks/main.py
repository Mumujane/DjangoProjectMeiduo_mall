from celery import Celery

import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'

# 创建celery 应用
app = Celery('meiduo')

# 导入celery配置
app.config_from_object('celery_tasks.config')

# 自动注册celery 任务
app.autodiscover_tasks(['celery_tasks.sms'])
