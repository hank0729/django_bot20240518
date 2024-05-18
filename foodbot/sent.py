from datetime import datetime
import re
import sqlite3
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import *
import os
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.configure(timezone=pytz.timezone('Asia/Taipei'))

DATABASE = 'data.db'

CHANNEL_ACCESS_TOKEN = 'LINE TOKEN'
CHANNEL_SECRET = 'LINE SECRET'

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

def get_db_connection():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with get_db_connection() as con:
        cursor = con.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS key (
                id INTEGER PRIMARY KEY,
                userid STRING,
                date STRING
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_info (
                user_id TEXT PRIMARY KEY,
                join_date DATE
            )
        ''')

init_db()

@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    join_date = datetime.now().strftime('%Y-%m-%d')
    
    with get_db_connection() as con:
        con.execute('''
            INSERT INTO user_info (user_id, join_date) 
            VALUES (?, ?) 
            ON CONFLICT(user_id) 
            DO UPDATE SET join_date = excluded.join_date
        ''', (user_id, join_date))
        con.commit()

    welcome_message = "歡迎加入！ 請填寫這份初步問卷，幫助我們更了解您。"
    form_url = "https://docs.google.com/forms/d/1tz_0tPbQ1c2p3Z6TF_LKOyqMo22jgDGlo0jgc6kRW4o/edit"
    message = TextSendMessage(text=f"{welcome_message}\n點擊這裡: {form_url}")
    line_bot_api.push_message(user_id, message)

def check_and_send_forms():
    now = datetime.now().date()
    with get_db_connection() as con:
        cursor = con.cursor()
        cursor.execute('SELECT user_id, join_date FROM user_info')
        users = cursor.fetchall()
        for user in users:
            user_id = user['user_id']
            join_date = datetime.strptime(user['join_date'], '%Y-%m-%d').date()
            days = (now - join_date).days
            
            if days in [7, 30, 60, 90]:
                if days % 7 == 0:
                    form_url = "https://docs.google.com/forms/d/12-MSdSVpeseFtY56murjtWGS24SwNRKdNAxvaGTg8Nc/edit"
                elif days == 30:
                    form_url = "https://docs.google.com/forms/u/0/d/1NV-KIUTrU1u5rMihasPnenwKfuP5Shecb6CJe5B4_-E/edit?pli=1"
                elif days == 60:
                    form_url = "https://docs.google.com/forms/d/1BJ7b4qMe2XY7o3mzxwwOb1wnGPkDWNV4ynbuC8emyyM/edit"
                elif days == 90:  
                    form_url = "https://docs.google.com/forms/d/1sjrRQYVQqWHCHR_uEx6wOfiVJU2AIoaAHl0CWtL5ThU/edit"
                else:
                    print('not the days')
                
                message = TextSendMessage(text=f"幫忙填個問卷吧!!\n {form_url}")
                line_bot_api.push_message(user_id, message)

scheduler.add_job(check_and_send_forms, 'cron', hour=7, minute=0)

scheduler.start()

# @app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# @handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id  
    message_text = event.message.text 
    reply_message = "Sorry, I didn't understand that."

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )


# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)
