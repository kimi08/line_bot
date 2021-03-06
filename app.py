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
import urllib

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


def pixabay_isch(event):
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        try:
            url = f"https://pixabay.com/images/search/{urllib.parse.urlencode({'q':event.message.text})[2:]}/"
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
            
            req = urllib.request.Request(url, headers = headers)
            conn = urllib.request.urlopen(req)
            
            print('fetch page finish')
            
            pattern = 'img srcset="\S*\s\w*,'
            img_list = []
            
            for match in re.finditer(pattern, str(conn.read())):
                img_list.append(match.group()[12:-3])
                
            random_img_url = img_list[random.randint(0, len(img_list)+1)]
            print('fetch img url finish')
            print(random_img_url)
            
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url=random_img_url,
                    preview_image_url=random_img_url
                )
            )
        # ????????????????????????????????????
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text)
            )
            pass



if __name__ == "__main__":
    app.run()