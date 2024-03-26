import os
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
import time
import json

os.environ["OPENAI_API_KEY"] = "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"

def generate_dalle(prompt1, save_path):
    try:
        client = OpenAI()
        print("Hola")

        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt1,
            n=2,
            size="1024x1024"
        )
        print("Hola11")
        # Loop over the response data
        for i, data in enumerate(response.data):
            # Extract the URL of the image
            image_url = data.url

            # Download the image
            image_response = requests.get(image_url)

            # Open the image
            image = Image.open(BytesIO(image_response.content))

            # Save the image with a unique filename
            image.save(os.path.join(save_path, f'image{i}.jpg'))
            
            image.show()
            
            time.sleep(5)
            
            image.close()

        print("Images saved")

    except Exception as e:
        print(f"An error occurred: {e}")
        


def chat_with_gpt(prompt):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a specialist in knowing songs just by the lyrics, i want you to answer me only with the name of the song and the artist."},
            {"role": "user", "content": prompt}
        ]
    )
    print(completion.choices[0].message)
    return completion.choices[0].message
# Example usage

def try_chat():
    api_key = "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"
    prompt = "What is the capital of France?"
    response = chat_with_gpt(api_key)
    print(f"Response: {response}")

if __name__ == "__main__":
    #generate_dalle("A dog", "Images")
    chat_with_gpt()
