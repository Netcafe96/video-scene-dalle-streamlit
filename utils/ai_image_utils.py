import openai, os
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_prompt_from_timecode(t):
    return f"An educational, realistic image representing a scene from a science video at {t} seconds."

def generate_image(prompt):
    r = openai.Image.create(prompt=prompt, n=1, size="512x512")
    return r['data'][0]['url']
