from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

# 若你已經安裝 python-dotenv，打開以下兩行來讀取 .env 設定
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))

@app.route("/")
def hello():
    return "LINE Webhook is working!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    print("[DEBUG] webhook body:", body)  # ✅ debug log

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    print("🔔 收到訊息：", event.message.text)
    print("👤 使用者 ID：", user_id)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"你的 LINE ID 是：{user_id}")
    )

if __name__ == "__main__":
    app.run(port=5000)
