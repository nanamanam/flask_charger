from flask import Flask, render_template, make_response,jsonify,request,session,redirect,flash,abort
import json
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
import config as cfg
line_api=cfg.line['line_api']
line_secret=cfg.line['line_secret']
line_bot_api = LineBotApi(line_api)
handler = WebhookHandler(line_secret)

def line_push(line_id,message):
    try:
        line_bot_api.push_message(line_id, TextSendMessage(text=message))
    except Exception as e:
        print(e)
        return e
    return 'Push success'