import cv2
import os
import base64
from dotenv import load_dotenv
import parse_system_prompt
import openai
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY in your .env file.")
openai.api_key = api_key

system_prompt = parse_system_prompt.parse_markdown_to_messages("system_prompt.md")

user_message = [
    {"role": "user",
    "content": [
        {
        "type": "text",
         "text": "This is the image of the pipe."
        },
        {
        "type": "image",
         "image": {
             "image_url": {
                 "url": parse_system_prompt.encode_image("./images/pipe_2.png")
                 }
            }
        },
        {
        "type": "text",
         "text": "This is the annotated image of the pipe, containing numbered bounding boxes with regions of interest within."
        },
        {
        "type": "image",
         "image": {
             "image_url": {
                 "url": parse_system_prompt.encode_image("./images/pipe_2_annotated.png")
                 }
            }
        },
        {
        "type": "text",
         "text": "Give me your analysis, as described in the system prompt."
        }
        ]
    }
]

system_prompt.extend(user_message)

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=system_prompt,
    temperature=0.5
)

print(response.choices[0].message.content)
raw_response = response.choices[0].message.content
raw_response = raw_response.replace("'", "\"")
detections = json.loads(raw_response)

# --- Step 6: Print the response ---
print("Image Analysis Response:")
print(detections)
