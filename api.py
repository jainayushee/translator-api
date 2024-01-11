from flask import Flask, json, request
from flask_cors import CORS
from dotenv import dotenv_values
import openai


config = dotenv_values(".env")
openai.api_key = config["API_KEY"]

api = Flask(__name__)
CORS(api)

@api.route('/', methods=['POST'])

def translate_text():
    text = request.json.get("text")
    source_language = request.json.get("source_language")
    target_language = request.json.get("target_language")
    prompt = f"Translate the following '{source_language}' text to '{target_language}': {text}"

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that translates text."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    translation = response.choices[0].message.content.strip()
    return json.dumps(translation)


if __name__ == '__main__':
    api.run()