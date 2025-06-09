import openai
import os

openai.api_key = os.getenv("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")

def generate_prompt_from_timecode(t):
    return f"A realistic, educational image illustrating a scene at {t} seconds of a science video."

def generate_image(prompt):
    r = openai.Image.create(prompt=prompt, n=1, size="512x512")
    return r['data'][0]['url']
