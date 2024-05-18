from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction
import logging
import time
import torch
import cv2
import shutil
import pandas as pd
import os
from datetime import datetime
from random import choices
import string
from openai import OpenAI
from .models import UserMessage, Main, First, Seven, Month, TwoMonth, ThreeMonth

domain = "https://06f9-122-121-6-6.ngrok-free.app/"
OPENAI_API_KEY = "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"
max_tokens = 500
temperature = 0

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

logger = logging.getLogger(__name__)
chat_language = os.getenv("INIT_LANGUAGE", default="zh")

conversation = []

class ChatGPT:
    def __init__(self, max_tokens, temperature):
        self.messages = conversation
        self.model = os.getenv("OPENAI_MODEL", default="gpt-3.5-turbo")
        self.max_tokens = max_tokens
        self.temperature = temperature

    def get_response(self, user_input):
        client = OpenAI(api_key=OPENAI_API_KEY)

        conversation = [{"role": "system", "content":'你是一個專業的醫療人員，請用已知的知識回答以下問題，若遇到不會的問題，請回答不清楚，請用繁體中文回答。'}, {"role": "user", "content": user_input}]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        print("AI回答內容：")
        print(response.choices[0].message.content)

        return response.choices[0].message.content


chatgpt = ChatGPT(max_tokens, temperature)

# 設定模型與資料導入
model_path = "./best.pt"
food_data = pd.read_excel("./food_data.xlsx")
food_dict = dict(food_data[["name", "fat"]].values)
food_name = dict(food_data[["name", "chinese_name"]].values)
model = torch.hub.load("ultralytics/yolov5", "custom", path=model_path)

@csrf_exempt
@require_http_methods(["POST"])
def callback(request):
    signature = request.headers['X-Line-Signature']
    body = request.body.decode('utf-8')
    logger.info(f"Request body: {body}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature. Please check your channel access token/channel secret.")
        return HttpResponse(status=400)

    return HttpResponse('OK', status=200)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text
    line_id = event.source.user_id
    UserMessage.objects.create(line_id=line_id, message_text=message_text)

@handler.add(FollowEvent)
def handle_follow(event):
    line_id = event.source.user_id
    
    def generate_random_key():
        part1 = 'm' 
        part2 = ''.join(choices(string.ascii_letters + string.digits, k=3))
        part3 = 'm'  
        part4 = ''.join(choices(string.ascii_letters + string.digits, k=3))
        return part1 + part2 + part3 + part4

    days = 1
    new_first = First.objects.create(lineid=line_id)  
    new_seven = Seven.objects.create(lineid=line_id)
    new_month = Month.objects.create(lineid=line_id)
    new_two_month = TwoMonth.objects.create(lineid=line_id)
    new_three_month = ThreeMonth.objects.create(lineid=line_id)

    main = Main.objects.create(
        lineid=line_id,
        days=days,
        first=new_first,
        first_key=new_first.id,  
        seven=new_seven,
        seven_key=new_seven.id,
        month=new_month,
        month_key=new_month.id,
        twomonth=new_two_month,
        twomonth_key=new_two_month.id,
        threemonth=new_three_month,
        threemonth_key=new_three_month.id
    )

    home_url = f"{settings.NGROK_HOST}/{line_id}/home/"
    line_bot_api.push_message(line_id, TextSendMessage(text=home_url))

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Thank you for adding me as a friend!")
    )

@csrf_exempt
@require_http_methods(["POST"])
def handle_submission(request, key, view_type):
    if view_type == 'first':
        model_class = First
    elif view_type == 'seven':
        model_class = Seven
    elif view_type == 'month':
        model_class = Month
    elif view_type == 'twomonth':
        model_class = TwoMonth
    elif view_type == 'threemonth':
        model_class = ThreeMonth
    else:
        return HttpResponse('Invalid view type', status=400)

    try:
        obj = get_object_or_404(model_class, id=key)
    except Http404:
        obj = model_class.objects.create()
        logger.info("Invalid key or view type, creating a new object.")

    for field in obj._meta.fields:
        if field.name in request.POST:
            setattr(obj, field.name, request.POST[field.name])

    obj.save()

    return HttpResponse('<center><h1>感謝回覆</h1></center>', status=200)

@csrf_exempt
def callback(request):
    if request.method == "POST":
        signature = request.META["HTTP_X_LINE_SIGNATURE"]
        body = request.body.decode("utf-8")

        try:
            events = parser.parse(body, signature)  # Parse the events
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent) and event.message.type == "image":
                image_content = line_bot_api.get_message_content(event.message.id)
                image_name = "0000.png"
                path = "./static/" + image_name
                with open(path, "wb") as fd:
                    for chunk in image_content.iter_content():
                        fd.write(chunk)
                img = cv2.imread(path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = model(img)
                result_df = results.pandas().xyxy[0]
                results.save()
                image = cv2.imread("./runs/detect/exp/image0.jpg")
                cv2.imwrite("./static/0000.png", image)
                messages = [
                    ImageSendMessage(
                        original_content_url=domain + "static/0000.png",
                        preview_image_url=domain + "static/0000.png",
                    )
                ]
                result_df["fat"] = result_df["name"].map(food_dict)
                result_df["chinese_name"] = result_df["name"].map(food_name)
                content = ""
                for i in range(len(result_df)):
                    name = result_df["chinese_name"][i]
                    fat = result_df["fat"][i]
                    food_content = f"{name} 熱量為 {fat} 大卡(kcals)"
                    content = content + food_content + "\n"
                total_fat = result_df["fat"].sum()
                total_content = f"總共: {total_fat} 大卡(kcals)"
                content = content + total_content
                messages.append(TextSendMessage(f"{content}"))
                messages.append(
                    TemplateSendMessage(
                        alt_text="Buttons template",
                        template=ButtonsTemplate(
                            title="請問是否正確?",
                            text="請問是否正確?",
                            actions=[
                                MessageTemplateAction(label="正確", text="正確"),
                                MessageTemplateAction(label="錯誤", text="錯誤"),
                            ],
                        ),
                    )
                )
                shutil.rmtree("./runs")
                line_bot_api.reply_message(event.reply_token, messages)
            elif isinstance(event, MessageEvent) and event.message.type == "text":
                if event.message.text in ["正確", "錯誤"]:
                    df = pd.read_excel("./datasets/label.xlsx")
                    T = time.ctime(time.time()).replace(" ", "-").replace(":", "-")
                    new_line = pd.DataFrame(
                        {"Column1": [T], "Column2": [event.message.text]}
                    )
                    df = pd.concat([df, new_line], ignore_index=True)
                    df.to_excel("./datasets/label.xlsx", index=False)
                    image = cv2.imread("./static/0000.png")
                    cv2.imwrite(f"./datasets/images/{T}.png", image)
                else:
                    user_message = event.message.text
                    reply_msg = chatgpt.get_response(user_message)
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text=reply_msg)
                    )
            elif isinstance(event, FollowEvent):
                line_id = event.source.user_id
                days = 1
                new_first = First.objects.create(lineid=line_id)
                new_seven = Seven.objects.create(lineid=line_id)
                new_month = Month.objects.create(lineid=line_id)
                new_two_month = TwoMonth.objects.create(lineid=line_id)
                new_three_month = ThreeMonth.objects.create(lineid=line_id)

                main = Main.objects.create(
                    lineid=line_id,
                    days=days,
                    first=new_first,
                    first_key=new_first.id,
                    seven=new_seven,
                    seven_key=new_seven.id,
                    month=new_month,
                    month_key=new_month.id,
                    twomonth=new_two_month,
                    twomonth_key=new_two_month.id,
                    threemonth=new_three_month,
                    threemonth_key=new_three_month.id
                )

                home_url = "https://" + f"{settings.NGROK_HOST}/{line_id}/home/"
                line_bot_api.push_message(line_id, TextSendMessage(text=home_url))

                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="感謝您加我好友!請幫忙填個問卷調查呦")
                )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id  
    message_text = event.message.text 
    reply_message = "Sorry, I didn't understand that."

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

from django.shortcuts import render, get_list_or_404

def home_view(request, name):
    mains = Main.objects.filter(lineid=name)
    if mains.exists():
        main = mains.first()  # Use the first object if multiple are returned
        context = {
            'first_key': main.first_key
        }
    else:
        context = {
            'first_key': None
        }

    return render(request, 'first.html', context)

def index_view(request, name):
    mains = Main.objects.filter(lineid=name)
    if mains.exists():
        main = mains.first()  
        context = {
            'seven_key': main.seven_key
        }
    else:
        context = {
            'seven_key': None
        }

    return render(request, 'seven.html', context)


def a3060_view(request, name):
    mains = Main.objects.filter(lineid=name)
    if mains.exists():
        main = mains.first()  # Use the first object if multiple are returned
        context = {
            'main': main,
            'TwoMonth_key': main.twomonth_key,
        }
    else:
        context = {
            'main': None,
            'TwoMonth_key': None,
        }

    return render(request, '3060.html', context)

def a90_view(request, name):
    mains = Main.objects.filter(lineid=name)
    if mains.exists():
        main = mains.first()  # Use the first object if multiple are returned
        context = {
            'main': main,
            'ThreeMonth_key': main.threemonth_key,
        }
    else:
        context = {
            'main': None,
            'ThreeMonth_key': None,
        }

    return render(request, '90.html', context)
