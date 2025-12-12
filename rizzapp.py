
import requests
import random
import json
from typing import Union
import re

def rizzer(text):
    formatted_query = text
    api = "https://dev-loopgpt.pantheonsite.io/wp-admin/js/RizzApp/rizz.php?text="
    response = requests.get(api + formatted_query)
    if response.status_code == 200:
        cleaned_response = response.text
        return cleaned_response
    else:
        return f"Error: {response.status_code}"


def extract_text(filename):
    api_key = random.choice(['d38b8514b288957', '6a48ab71af88957'])
    url_api = "https://api.ocr.space/parse/image"
    with open(filename, 'rb') as image_file:
        result = requests.post(
            url_api,
            files={filename: image_file},
            data={
                'apikey': api_key,
                'language': 'eng',
            }
        )

    result = result.json()
    if result.get('IsErroredOnProcessing'):
        return "Error: " + result.get('ErrorMessage')[0]

    return result.get('ParsedResults')[0].get('ParsedText')


def format(json_lines: Union[str, bytes], encoding: str = "utf-8") -> str:
    if isinstance(json_lines, bytes):
        json_lines = json_lines.decode(encoding)

    lines = json_lines.strip().split("\n")
    tokens = []

    for line in lines:
        try:
            
            data = json.loads(line, strict=False)
            if data.get("type") == "stream" and "token" in data:
                token = re.sub(r'\x00+', '', data["token"])
                try:
                    token = token.encode("latin1").decode("utf-8")
                except (UnicodeEncodeError, UnicodeDecodeError):
                    pass 
                tokens.append(token)
        except json.JSONDecodeError as e:
            print(f"Skipping malformed line: {line} | Error: {e}")
            continue  

    return ''.join(tokens).strip()


def trans(text):
    """
    Translates using the unofficial Google Translate API.
    This API auto-detects the source language.
    """
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "auto",
        "tl": "en",
        "dt": "t",
        "q": text
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()
        translated = ''.join([item[0] for item in result[0] if item[0]])
        return translated
    except Exception as e:
        print("Error during translation:", e)
        return None


def trim_string(s: str) -> str:

    if len(s) <= 4:
        return ""
    return s[2:-2]


filepath= input("Your Chat Screenchot Path:")

a=rizzer(extract_text(filepath))
print("RizzApp would Say: "+ a)