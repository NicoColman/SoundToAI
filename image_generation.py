import requests
from PIL import Image
import io
import os

def generate_image(prompt, save_path):
    # Define the API endpoint
    url = "https://api.deepai.org/api/text2img"

    # Define the headers for the API request
    headers = {
        "api-key": "b6bc8f3d-eaf5-40a3-91be-e5b68301b186"  # Replace with your actual API key
    }

    # Define the body of the API request
    body = {
        "text": prompt
    }

    # Make the API request
    response = requests.post(url, headers=headers, data=body)
    print(response.text)

   # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()

        # Extract the URL of the generated image
        image_url = data["output_url"]

        # Download the image
        image_response = requests.get(image_url)

        image = Image.open(io.BytesIO(image_response.content))
        width, height = image.size
        image = image.crop((0, 0, width // 2, height // 2))

        # Save the image to a file
        image.save(os.path.join(save_path, 'image.jpg'))

        print(f"Image saved as {save_path}")
        return image_url
    else:
        print(f"Image generation failed with status code {response.status_code}")
        return None
    

if __name__ == "__main__":
    generate_image('Images')