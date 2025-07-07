import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_image(prompt: str) -> str:
    resp = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="512x512"  # or "1024x1024"
    )
    return resp["data"][0]["url"]
