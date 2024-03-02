from openai import OpenAI
from Speech_to_text import Speech_to_text
client = OpenAI()

def image(prompt):
    response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1,
    )

    image_url = response.data[0].url
    return image_url

def image_editing(prompt,image_path):
    response = client.images.edit(
        model="dall-e-2",
        image=open(image_path, "rb"),
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response.data[0].url
    return image_url