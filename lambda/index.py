import json
import urllib.request

API_URL = "https://a650-34-169-49-73.ngrok-free.app/generate"

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        # リクエストボディを取得
        body = json.loads(event["body"])
        message = body["message"]

        # FastAPI /generate に送る形式に変換
        request_data = json.dumps({
            "prompt": message,
            "max_new_tokens": 512,
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 0.9
        }).encode("utf-8")

        # リクエスト送信
        req = urllib.request.Request(
            API_URL,
            data=request_data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req) as response:
            res_body = response.read()
            result = json.loads(res_body.decode("utf-8"))

        generated_text = result.get("generated_text", "")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": generated_text,
                "conversationHistory": [
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": generated_text}
                ]
            })
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "success": False,
                "error": str(e)
            })
        }

