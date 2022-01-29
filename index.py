import logging
import json
import base64
import requests
import re

bili_url = "http://api.bilibili.com/x/space/acc/info"
#b站用户的uid, 多个id逗号分割
bili_live_idx = ['692283831']


def handler(event, context):
    request = json.loads(event)
    logger = logging.getLogger()
    body = base64.b64decode(request['body']).decode()
    data = json.loads(body)
    logger.info(data)
    reply_str = cache()
    response = {
        "isBase64Encoded": "false",
        "statusCode": "200",
        "headers": {"content-type": "application/json"},
        "body": {
            "returnCode": "0",
            "returnErrorSolution": "",
            "returnMessage": "",
            "returnValue": {
                "reply": reply_str,
                "resultType": "RESULT",
                "executeCode": "SUCCESS",
                "msgInfo": ""
            }
        }
    }
    print(response)
    return response

def get_bili_status(uid):
    return requests.get(bili_url, params={'mid': uid}).json()

def cache():
    vtbs = []
    title = '您关注的'
    for uid in bili_live_idx:
        resp_json = get_bili_status(uid)
        status = resp_json['data']['live_room']['liveStatus']
        if status == 1:
            vtbs.append(resp_json['data']['name'])
    if len(vtbs)>0:
        split = ','
        title = title + split.join(vtbs) +'开播了!'
    else:
        title = '没有人开播'
    return title
    
if __name__ == "__main__":
    print(cache())
