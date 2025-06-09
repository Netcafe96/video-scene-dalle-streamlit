import openai, os
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_prompt_from_timecode(t):
    return f"Educational realistic image illustrating a scene at {t} seconds of a science video."

def generate_image(prompt):
    res = openai.Image.create(prompt=prompt, n=1, size="512x512")
    return res['data'][0]['url']
