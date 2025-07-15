import boto3
import os
import json
from dotenv import load_dotenv

load_dotenv()

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name=os.getenv("AWS_DEFAULT_REGION")
)

model_id = os.getenv("BEDROCK_MODEL_ID")

messages = [
    {"role": "user", "content": "What's the capital of Canada?"}
]

body = {
    "messages": messages,
    "anthropic_version": "bedrock-2023-05-31",  # required for Claude models
    "max_tokens": 100
}

response = bedrock_runtime.invoke_model(
    modelId=model_id,
    body=json.dumps(body),
    contentType="application/json",
    accept="application/json"
)

response_body = json.loads(response["body"].read().decode())
print(response_body["content"][0]["text"])
