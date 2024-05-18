from celery import shared_task
from .models import Main
from django.conf import settings
from linebot import LineBotApi
from linebot.models import TextSendMessage
import logging

logger = logging.getLogger(__name__)

# 添加调试信息
logger.info(f"LINE_CHANNEL_ACCESS_TOKEN: {settings.LINE_CHANNEL_ACCESS_TOKEN}")
logger.info(f"NGROK_HOST: {settings.NGROK_HOST}")

# 确保能正确读取 LINE_CHANNEL_ACCESS_TOKEN
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

@shared_task
def increment_days():
    mains = Main.objects.all()
    for main in mains:
        main.days += 1

        if main.days >= 1 and main.first == 1:
            main.first = 0
            message = f"{settings.NGROK_HOST}/{main.first_key}/home"
            line_bot_api.push_message(main.lineid, TextSendMessage(text=message))

        n = main.days // 7
        if main.seven < n:
            main.seven = n
            message = f"{settings.NGROK_HOST}/{main.seven_key}/index"
            line_bot_api.push_message(main.lineid, TextSendMessage(text=message))

        if main.days >= 30 and main.month == 0:
            main.month = 1
            message = f"{settings.NGROK_HOST}/{main.month_key}/a3060"
            line_bot_api.push_message(main.lineid, TextSendMessage(text=message))

        if main.days >= 60 and main.twomonth == 0:
            main.twomonth = 1
            message = f"{settings.NGROK_HOST}/{main.twomonth_key}/a3060"
            line_bot_api.push_message(main.lineid, TextSendMessage(text=message))

        if main.days >= 90 and main.threemonth == 0:
            main.threemonth = 1
            message = f"{settings.NGROK_HOST}/{main.threemonth_key}/a90"
            line_bot_api.push_message(main.lineid, TextSendMessage(text=message))

        main.save()