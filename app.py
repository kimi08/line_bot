from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('yVkxKFdC9d5y+oOKRKMoCsqk+sCUUzBdoVTx9K9lI8q7s6otLV6JwPkvHT80IfTfeqxyaUQpNEwrCA9j4ASJaV57VOgLR3vhUd0kN+bSRR//ur8nfvBJz+f3gmEPyIeMLQ3ghYuVEV7DdM7+UaOG8AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3445ef72390ef8e8922ed0ae753ab4f0')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()