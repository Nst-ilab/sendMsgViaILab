import boto3
import json
import re

#Region指定しないと、デフォルトのUSリージョンが使われる
clientLambda = boto3.client('lambda', region_name='ap-northeast-1')

def lambda_handler(event, context):
    lineMessage = event["lineMessage"]["events"][0]["message"]["text"]
    
    matchObj = re.search("へ( |　)", lineMessage)
    print(matchObj)
    
    if matchObj == None:
        return None
    index = matchObj.start()
    key = lineMessage[:index]
    print(key)
    
    # 引数としてkey(名前)を渡す
    input_event = {
        "key":key
    }
    Payload = json.dumps(input_event) # jsonシリアライズ
     
    # strageGet関数呼び出し
    response = clientLambda.invoke(
        # Calleeのarnを指定
        FunctionName='cloud9-storageDao-storageGet-SV2WOCWTIT0Z',
         # RequestResponse = 同期、Event = 非同期 で実行できます
        InvocationType='RequestResponse',
        Payload=Payload
    )
     
    # レスポンス読出し
    response_payload = json.loads(response["Payload"].read()) # jsonデコード
    
    if response_payload is None:
        return None
    
    #pushMessage呼出
    if lineMessage[index+2:] == "": #メッセージが入力されていない場合
       return None
    
    input_event = {
         "to" : response_payload,
            "messages": {
                "type": "text",
                "text": lineMessage[index+2:]
            }
    }
    Payload = json.dumps(input_event) # jsonシリアライズ
    
    # pushMessage関数呼び出し
    response = clientLambda.invoke(
        # Calleeのarnを指定
        FunctionName='cloud9-pushMessage-pushMessage-QFAN7KZ9AW5U',
        # RequestResponse = 同期、Event = 非同期 で実行できます
        InvocationType='RequestResponse',
        Payload=Payload
    )
    
     # レスポンス読出し
    response_payload = json.loads(response["Payload"].read()) # jsonデコード
    print(response_payload)
    if response_payload == False:
        return None
    else :
        return {"message":"送信が成功しました"}
        
    
    