# 正直よくわかりませんでした！
import urllib.request
import json

# FastAPIのエンドポイント (ここに実際のURLを指定してください)
FASTAPI_ENDPOINT = "https://d3tuv0dd8vyrve.cloudfront.net/"

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        # Cognito認証ユーザー情報の取得（元コードを維持、ログのみ）
        user_info = None
        if 'requestContext' in event and 'authorizer' in event['requestContext']:
            user_info = event['requestContext']['authorizer']['claims']
            print(f"Authenticated user: {user_info.get('email') or user_info.get('cognito:username')}")

        # リクエストボディの解析
        body = json.loads(event['body'])
        message = body['message']
        conversation_history = body.get('conversationHistory', [])

        print("Processing message:", message)
        print("Forwarding request to FastAPI endpoint:", FASTAPI_ENDPOINT)

        # FastAPIに送信するペイロードの準備
        request_payload = json.dumps({
            "message": message,
            "conversationHistory": conversation_history
        }).encode('utf-8')

        # urllib.requestでFastAPIを呼び出す
        req = urllib.request.Request(
            FASTAPI_ENDPOINT,
            data=request_payload,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        with urllib.request.urlopen(req) as response:
            fastapi_response = json.loads(response.read().decode('utf-8'))

        print("Received response from FastAPI:", fastapi_response)

        # FastAPIからのレスポンスをそのままクライアントに返却
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps(fastapi_response)
        }

    except Exception as error:
        print("Error:", str(error))

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }
