import cv2
import os
import base64
from dotenv import load_dotenv
import feature_detection
import parse_system_prompt
import openai
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY in your .env file.")
openai.api_key = api_key

system_prompt = parse_system_prompt.parse_markdown_to_messages("system_prompt.md")

image = cv2.imread("./other/pipe_image_1.png", cv2.IMREAD_UNCHANGED)
boxes, annotated_image = feature_detection.get_bounding_boxes(image)
cv2.imwrite("image.jpg", image)
cv2.imwrite("image_annotated.jpg", annotated_image)

user_message = {"role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": "This is the image of the pipe."
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": parse_system_prompt.encode_image("image.jpg")
                        }
                    },
                    {
                    "type": "text",
                    "text": "This is the annotated image of the pipe, containing numbered bounding boxes with regions of interest within."
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": parse_system_prompt.encode_image("image_annotated.jpg")
                        }
                    },
                    {
                    "type": "text",
                    "text": "Give me your analysis, as described in the system prompt."
                    }
                    ]
                }

system_prompt.append(user_message)

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=system_prompt,
    temperature=0.5
)

raw_response = response.choices[0].message.content
raw_response = raw_response.replace("'", "\"")
detections = json.loads(raw_response)

labeled_image = feature_detection.label_boxes(annotated_image, boxes, detections)


cv2.imwrite("image_labeled.jpg", labeled_image)
cv2.imshow("labeled image", labeled_image)
cv2.waitKey(0)
cv2.destroyAllWindows()