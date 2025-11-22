import requests
import os
import uuid
from typing import Optional
import json

from dotenv import load_dotenv
load_dotenv()

BASE_API_URL = "https://aws-us-east-2.langflow.datastax.com"
LANGFLOW_ID = "dd9f6507-4d5c-4d30-ac65-28c56be5756f"
APPLICATION_TOKEN = os.getenv('MACROS_API_TOKEN')

def dict_to_string(obj, level=0):
    strings = []
    indent = "  " * level
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                nested_string = dict_to_string(value, level + 1)
                strings.append(f"{indent}{key}: {nested_string}")
            else:
                strings.append(f"{indent}{key}: {value}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            nested_string = dict_to_string(item, level + 1)
            strings.append(f"{indent}Item {idx + 1}: {nested_string}")
    else:
        strings.append(f"{indent}{obj}")

    return ", ".join(strings)

def askAI(profile, question):
    url = "https://aws-us-east-2.langflow.datastax.com/lf/dd9f6507-4d5c-4d30-ac65-28c56be5756f/api/v1/run/ed8c2cba-4583-428f-af7c-70adb6437a70"  # The complete API endpoint URL for this flow

    headers = { 
        "X-DataStax-Current-Org": "e3c83f74-0361-4cc8-a495-ac80d69d7ea8", 
        "Authorization": f"Bearer {os.getenv('ASKAI_API_TOKEN')}", 
        "Content-Type": "application/json", 
        "Accept": "application/json", 
    }
    
    # Request payload configuration
    payload = {
        "output_type": "chat",
        "input_type": "text",
        "tweaks": {
            "TextInput-UKbPZ": {
                "input_value": question
            },
            "TextInput-g5Juo": {
                "input_value": dict_to_string(profile)
            }
        }
    }
    payload["session_id"] = str(uuid.uuid4())
    return requests.request("POST", url, json=payload, headers=headers)

def get_macros(profile, goals):
    url = "https://aws-us-east-2.langflow.datastax.com/lf/dd9f6507-4d5c-4d30-ac65-28c56be5756f/api/v1/run/macros"  # The complete API endpoint URL for this flow

    headers = { 
        "X-DataStax-Current-Org": "e3c83f74-0361-4cc8-a495-ac80d69d7ea8", 
        "Authorization": f"Bearer {os.getenv('MACROS_API_TOKEN')}", 
        "Content-Type": "application/json", 
        "Accept": "application/json", 
    }
    # Request payload configuration
    print("Goals:", ', '.join(goals))
    print("Profile:", dict_to_string(profile))
    payload = {
        "output_type": "text",
        "input_type": "text",
        "tweaks": {
            "TextInput-Wi2T3": {
                "input_value": ', '.join(goals)
            },
            "TextInput-aTKLP": {
                "input_value": dict_to_string(profile)
            }
        }
    }
    payload["session_id"] = str(uuid.uuid4())

    response = requests.post(url, json=payload, headers=headers)
    print("AI Response:", response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"])
    return json.loads(response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"])

    # return run_flow("",
    #   tweaks=payload["tweaks"], 
    #   application_token=APPLICATION_TOKEN)




# payload = get_macros("Maintain weight at 2000 calories per day, with 40% carbs, 30% protein, and 30% fats.", "muscle gain")
# url = "https://aws-us-east-2.langflow.datastax.com/lf/dd9f6507-4d5c-4d30-ac65-28c56be5756f/api/v1/run/macros"


# try:
#     # Send API request
#     response = payload
#     response.raise_for_status()  # Raise exception for bad status codes

#     # Print response
#     print(response.text)

# except requests.exceptions.RequestException as e:
#     print(f"Error making API request: {e}")
# except ValueError as e:
#     print(f"Error parsing response: {e}")

